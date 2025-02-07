-- Fix tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    priority VARCHAR(10) CHECK (priority IN ('RED', 'ORANGE', 'YELLOW', 'GREEN')),
    status VARCHAR(20) DEFAULT 'pending',
    due_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create voice_patterns table
CREATE TABLE IF NOT EXISTS voice_patterns (
    id SERIAL PRIMARY KEY,
    pattern_type VARCHAR(50) NOT NULL,
    pattern_data JSONB NOT NULL,
    is_active BOOLEAN DEFAULT true
);

-- Create voice_settings table
CREATE TABLE IF NOT EXISTS voice_settings (
    id SERIAL PRIMARY KEY,
    settings_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create russ_management tables
CREATE TABLE IF NOT EXISTS russ_status (
    id SERIAL PRIMARY KEY,
    status_data JSONB NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS russ_medications (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    schedule JSONB NOT NULL,
    active BOOLEAN DEFAULT true
);

CREATE TABLE IF NOT EXISTS russ_activities (
    id SERIAL PRIMARY KEY,
    activity_type VARCHAR(50) NOT NULL,
    activity_data JSONB NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create data_sync_log table
CREATE TABLE IF NOT EXISTS data_sync_log (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL,
    details JSONB
); 