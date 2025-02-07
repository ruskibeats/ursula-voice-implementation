#!/bin/bash

# Production Setup Script for Ursula's Task Management System

# Exit on error
set -e

echo "Setting up Ursula's Task Management System for production..."

# Install system dependencies
apt-get update
apt-get install -y \
    python3-pip \
    python3-venv \
    supervisor \
    nginx \
    sqlite3 \
    systemd \
    git \
    build-essential \
    libssl-dev

# Create service user
useradd -r -s /bin/false ursula_service || true

# Create application directories
mkdir -p /opt/ursula/
mkdir -p /opt/ursula/logs
mkdir -p /opt/ursula/db
mkdir -p /var/log/ursula

# Set up virtual environment
python3 -m venv /opt/ursula/venv
source /opt/ursula/venv/bin/activate

# Install Python dependencies with specific versions
pip install -r requirements.txt

# Copy application files
cp -r * /opt/ursula/
cp ursula.db /opt/ursula/db/

# Set up systemd service
cat > /etc/systemd/system/ursula.service << EOL
[Unit]
Description=Ursula Task Management System
After=network.target

[Service]
Type=notify
User=ursula_service
Group=ursula_service
WorkingDirectory=/opt/ursula
Environment="PATH=/opt/ursula/venv/bin"
ExecStart=/opt/ursula/venv/bin/uvicorn ursula_api:app --host 0.0.0.0 --port 8080 --workers 4 --log-level warning
Restart=always
RestartSec=5
StartLimitInterval=0
WatchdogSec=30

# Security hardening
PrivateTmp=true
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target
EOL

# Set up supervisor (backup process manager)
cat > /etc/supervisor/conf.d/ursula.conf << EOL
[program:ursula]
command=/opt/ursula/venv/bin/uvicorn ursula_api:app --host 0.0.0.0 --port 8080 --workers 4
directory=/opt/ursula
user=ursula_service
autostart=true
autorestart=true
stderr_logfile=/var/log/ursula/err.log
stdout_logfile=/var/log/ursula/out.log
environment=PATH="/opt/ursula/venv/bin"

[supervisord]
logfile=/var/log/supervisor/supervisord.log
pidfile=/var/run/supervisord.pid
childlogdir=/var/log/supervisor
EOL

# Set up log rotation
cat > /etc/logrotate.d/ursula << EOL
/var/log/ursula/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 ursula_service ursula_service
    sharedscripts
    postrotate
        supervisorctl restart ursula
    endscript
}
EOL

# Set up monitoring script
cat > /opt/ursula/monitor.sh << EOL
#!/bin/bash
# Health check and auto-recovery script

check_service() {
    if ! curl -s http://localhost:8080/health > /dev/null; then
        echo "\$(date): Service health check failed. Restarting..." >> /var/log/ursula/monitor.log
        systemctl restart ursula
        sleep 10
        if ! curl -s http://localhost:8080/health > /dev/null; then
            echo "\$(date): Service failed to recover. Falling back to supervisor..." >> /var/log/ursula/monitor.log
            supervisorctl restart ursula
        fi
    fi
}

# Monitor DB connection
check_db() {
    if ! sqlite3 /opt/ursula/db/ursula.db "SELECT 1;" > /dev/null 2>&1; then
        echo "\$(date): Database check failed. Attempting recovery..." >> /var/log/ursula/monitor.log
        cp /opt/ursula/db/ursula.db.backup /opt/ursula/db/ursula.db
        systemctl restart ursula
    fi
}

# Run checks every minute
while true; do
    check_service
    check_db
    sleep 60
done
EOL

chmod +x /opt/ursula/monitor.sh

# Set up backup script
cat > /opt/ursula/backup.sh << EOL
#!/bin/bash
# Database backup script

BACKUP_DIR="/opt/ursula/db/backups"
mkdir -p \$BACKUP_DIR

# Create timestamped backup
TIMESTAMP=\$(date +%Y%m%d_%H%M%S)
sqlite3 /opt/ursula/db/ursula.db ".backup '/opt/ursula/db/backups/ursula_\${TIMESTAMP}.db'"

# Keep latest backup as quick recovery option
cp /opt/ursula/db/backups/ursula_\${TIMESTAMP}.db /opt/ursula/db/ursula.db.backup

# Clean old backups (keep last 7 days)
find \$BACKUP_DIR -name "ursula_*.db" -mtime +7 -delete
EOL

chmod +x /opt/ursula/backup.sh

# Set up cron jobs
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/ursula/backup.sh") | crontab -
(crontab -l 2>/dev/null; echo "@reboot /opt/ursula/monitor.sh") | crontab -

# Set correct permissions
chown -R ursula_service:ursula_service /opt/ursula
chmod -R 750 /opt/ursula
chmod 660 /opt/ursula/db/ursula.db

# Start services
systemctl daemon-reload
systemctl enable ursula
systemctl start ursula
systemctl start supervisor
supervisorctl reread
supervisorctl update

# Start monitoring
/opt/ursula/monitor.sh & 

echo "Production setup complete. Service is running and monitored."
echo "Check status with: systemctl status ursula"
echo "View logs with: tail -f /var/log/ursula/out.log" 