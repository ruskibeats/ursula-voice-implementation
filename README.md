# Ursula's Task Management System

## Overview
An AI-powered task management system that embodies Ursula O'Sullivan's unique approach to managing family chaos and ADHD challenges. The system combines structured data management with AI-driven contextual enrichment.

## Server Management

### Starting the Server
```bash
# Start in foreground
python3 ursula_api.py

# Start in background
python3 ursula_api.py &

# Start with uvicorn directly
uvicorn ursula_api:app --host 0.0.0.0 --port 8080 --reload
```

### Stopping the Server
```bash
# Graceful shutdown (if running in foreground)
Ctrl+C

# Kill all Python processes
pkill -9 python3

# Find and kill specific process
ps aux | grep "ursula_api.py"
kill -9 <process_id>
```

### Database Reset
```bash
# Stop server, delete DB, and restart
pkill -9 python3 && rm -f ursula.db && python3 ursula_api.py

# Clean start (one-liner)
pkill -9 python3 && rm -f ursula.db && python3 ursula_api.py &
```

### Health Check
```bash
# Check if server is running
curl http://localhost:8080/docs

# Check specific endpoint
curl http://localhost:8080/universe/family
```

## Core Components

### 1. Database Structure
- **Tasks & Metadata**
  - Core task tracking
  - Historical interactions
  - Success patterns
  - Voice patterns and effectiveness
  - Relationship impacts

- **Learning System**
  - Task patterns and effectiveness
  - Family member responses
  - Time-based patterns
  - Voice pattern effectiveness

- **Context Management**
  - Family relationships
  - Location significance
  - Historical references
  - Trust levels

### 2. AI Enrichment
- Task contextualization
- Voice pattern selection
- Story/anecdote matching
- Urgency assessment
- Family impact analysis

### 3. Voice System
- SSML patterns for different contexts
- Mood-based adjustments
- Family member specific patterns
- Success tracking

## Current State

### Implemented Features
- Basic task management
- Family relationship tracking
- Voice pattern system
- Initial AI enrichment
- Basic learning system

### Database Tables
- `core_identity`
- `characters`
- `locations`
- `relationships`
- `tasks`
- `task_history`
- `voice_patterns`
- `family_chaos`
- `task_effectiveness`

## Roadmap

### Phase 1: Enhanced Learning
- [ ] Pattern recognition improvements
- [ ] Success rate tracking
- [ ] Voice pattern effectiveness
- [ ] Family response patterns

### Phase 2: Context Enrichment
- [ ] Better story matching
- [ ] Relationship impact tracking
- [ ] Location significance
- [ ] Time-based patterns

### Phase 3: Voice System
- [ ] Dynamic SSML generation
- [ ] Mood-based adjustments
- [ ] Family-specific patterns
- [ ] Success tracking

## API Endpoints

### Task Management
- `GET /tasks` - List all tasks
- `GET /tasks/{priority}` - Get tasks by priority
- `POST /tasks/process` - Process and enrich tasks
- `GET /tasks/rollcall` - Generate roll call script

### Voice System
- `GET /voice/patterns/{tag_type}` - Get voice patterns
- `POST /tasks/ai_enrich` - AI enrichment for tasks

### Family Management
- `GET /russ/family` - Family chaos patterns
- `GET /russ/patterns` - ADHD patterns
- `GET /russ/triggers` - Escalation triggers

## Integration Points

### n8n Workflows
- Task processing
- Voice pattern selection
- Learning system updates
- Context enrichment

### AI Integration
- OpenAI for context generation
- Voice pattern selection
- Story matching
- Urgency assessment

## Development

### Prerequisites
- Python 3.8+
- PostgreSQL
- FastAPI
- n8n

### Setup
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up PostgreSQL database
4. Initialize database: `python init_db.py`
5. Start server: `uvicorn ursula_api:app --reload`

### Environment Variables
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/ursula
AI_API_KEY=your_openai_key
VOICE_API_KEY=your_voice_api_key
```

## Contributing
1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License
MIT License

## Acknowledgments
- Ursula O'Sullivan character concept
- FastAPI framework
- n8n workflow automation
- OpenAI for AI capabilities
