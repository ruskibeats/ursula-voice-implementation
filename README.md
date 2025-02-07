# Ursula's Task Management System

## Latest Checkpoint (2024-02-07)

### Added
- Trust system schema and data population
- Relationship management system
- Story management with background stories
- Character backstories and locations
- Task management system with priorities
- Voice pattern system with SSML templates
- AI delegation schema

### Changed
- Updated database schema to support complex relationships
- Enhanced task management with escalation system
- Improved character profile management

### Fixed
- Table alias issues in SQL queries
- Database connection handling
- Schema consistency across tables

## Overview
An AI-powered task management system that embodies Ursula O'Sullivan's unique approach to managing family chaos and ADHD challenges. The system combines structured data management with AI-driven contextual enrichment.

## Quick Start

```bash
# Clone the repository
git clone [repository-url]
cd scripts

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
sqlite3 ursula.db < combined_schema.sql

# Start server
python3 -m uvicorn ursula_api:app --host 0.0.0.0 --port 8080 --reload
```

## API Documentation

### Health Check
```http
GET /health
```
Returns system health status including database connection, memory usage, and disk space.

Response:
```json
{
    "status": "healthy",
    "database": "connected",
    "memory": 63.3,
    "disk": 9.18,
    "timestamp": "2025-02-06T10:28:31.483975Z"
}
```

### Universe APIs

#### Get Family Members
```http
GET /universe/family
```
Returns list of family members and their relationships to Ursula.

#### Get Characters
```http
GET /universe/characters
```
Returns list of recurring characters in Ursula's world.

#### Get Locations
```http
GET /universe/locations
```
Returns significant locations and their details.

#### Get Rules
```http
GET /universe/rules
```
Returns Ursula's personal rules and guidelines.

#### Get Relationships
```http
GET /universe/relationships
```
Returns Ursula's relationship network.

### Task Management APIs

#### Get Tasks by Priority
```http
GET /tasks/{priority}
```
Returns tasks filtered by priority level (RED, ORANGE, YELLOW, GREEN).

#### Get Task Escalations
```http
GET /tasks/escalations/{type}
```
Returns escalation patterns for specific task types.

#### Get All Tasks
```http
GET /tasks
```
Returns all active tasks.

#### Get Task Subtasks
```http
GET /tasks/subtasks/{task_id}
```
Returns subtasks for a specific task.

#### Complete Task
```http
PUT /tasks/{task_id}/complete
```
Marks a task as completed.

#### Update Task Notes
```http
PUT /tasks/{task_id}/notes
```
Updates notes for a specific task.

### Voice Pattern APIs

#### Get Voice Patterns
```http
GET /voice/patterns/{tag_type}
```
Returns SSML patterns for specific emotion types.

### Russ Management APIs

#### Get Character Profiles
```http
GET /russ/profiles
```
Returns character profiles related to Russ.

#### Get ADHD Patterns
```http
GET /russ/patterns
```
Returns ADHD behavior patterns.

#### Get Escalation Triggers
```http
GET /russ/triggers
```
Returns triggers that require escalation.

#### Get Failure Stories
```http
GET /russ/stories
```
Returns cautionary tales and success stories.

### Data Ingestion APIs

#### Ingest Raw Data
```http
POST /ingest/raw
```
Ingests raw data from various sources.

#### Get Ingestion Status
```http
GET /ingest/status/{ingest_id}
```
Returns status of data ingestion process.

#### Get Pending Ingestions
```http
GET /ingest/pending
```
Returns list of pending data ingestions.

### Webhook APIs

#### Handle Webhook
```http
POST /webhook/{source}
```
Handles incoming webhooks from various sources.

#### Get Webhook Config
```http
GET /webhook/config/{source}
```
Returns webhook configuration for specific source.

## Environment Variables
```env
DATABASE_URL=sqlite:///ursula.db
SENTRY_DSN=[your-sentry-dsn]
LOG_LEVEL=INFO
```

## Database Schema
See `combined_schema.sql` for complete database structure.

## Development

### Code Style
- Black for Python formatting
- Flake8 for linting
- MyPy for type checking

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=.
```

### Logging
Structured logging with JSON format:
```json
{
    "event": "Starting Ursula's Task Management System...",
    "timestamp": "2025-02-06T10:28:31.483975Z"
}
```

## Production Deployment
See `setup.sh` for complete production setup script.

## Monitoring
- Health check endpoint at `/health`
- Prometheus metrics at `/metrics`
- Sentry integration for error tracking

## Security
- CORS configuration
- Rate limiting
- Input validation
- Secure headers

## License
[License Type]

## Contributing
[Contributing Guidelines]

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

### 1. Data Ingestion
- **Raw Data Ingestion**
  - Flexible JSON ingestion
  - Priority-based processing
  - Status tracking
  - Async processing pipeline

- **Webhook Integration**
  - Todoist integration
  - Email processing
  - Calendar sync
  - Real-time updates

### 2. Task Management
- Priority levels (🔥 RED to 🟢 GREEN)
- Task enrichment
- Voice pattern selection
- Family impact analysis

### 3. AI Enrichment
- Task contextualization
- Voice pattern selection
- Story/anecdote matching
- Urgency assessment

### 4. Voice System
- SSML patterns
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

### Data Ingestion
```bash
# Raw Data Ingestion
POST /ingest/raw
GET /ingest/status/{id}
GET /ingest/pending

# Webhooks
POST /webhook/{source}
GET /webhook/config/{source}
```

### Task Management
```bash
# Task Operations
GET /tasks
GET /tasks/{priority}
POST /tasks/process
GET /tasks/rollcall

# Todoist Integration
POST /tasks/todoist/import/full
GET /tasks/todoist/sync
```

### Voice System
```bash
GET /voice/patterns/{tag_type}
POST /tasks/ai_enrich
```

## Webhook Integration

### 1. Todoist Webhook
```bash
curl -X POST http://192.168.0.63:8080/webhook/todoist \
-H "Content-Type: application/json" \
-H "X-Signature: YOUR_SIGNATURE" \
-d '{
    "event_type": "item:added",
    "data": {
        "content": "Medical appointment",
        "priority": 4,
        "due": "2024-03-20"
    }
}'
```

### 2. Email Webhook
```bash
curl -X POST http://192.168.0.63:8080/webhook/email \
-H "Content-Type: application/json" \
-d '{
    "event_type": "new_email",
    "data": {
        "subject": "Urgent: Medical Appointment",
        "body": "Reminder for tomorrow"
    }
}'
```

## Raw Data Ingestion

### 1. Direct Ingestion
```bash
curl -X POST http://192.168.0.63:8080/ingest/raw \
-H "Content-Type: application/json" \
-d '{
    "source": "email",
    "content": {
        "tasks": [{
            "content": "Medical appointment",
            "urgent": true,
            "due_date": "2024-03-20"
        }]
    },
    "priority": "urgent"
}'
```

### 2. Check Status
```bash
curl http://192.168.0.63:8080/ingest/status/1
```

### 3. View Pending
```bash
curl http://192.168.0.63:8080/ingest/pending
```

## Development

### Prerequisites
- Python 3.8+
- FastAPI
- SQLite/PostgreSQL
- n8n for workflows

### Setup
```bash
# Clone repository
git clone https://github.com/your-repo/ursula-system.git

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Start server
python ursula_api.py
```

### Environment Variables
```env
DATABASE_URL=sqlite:///./ursula.db
TODOIST_API_TOKEN=your_token_here
```

## Configuration

### Database Configuration
```sql
# Core Tables
- tasks
  - Priority tracking (🔥 RED to 🟢 GREEN)
  - Task metadata
  - Processing status

- raw_data
  - Flexible JSON storage
  - Processing status
  - Priority tracking
  - Metadata fields

- patterns
  - SSML voice patterns
  - Success tracking
  - Context mapping
```

### Webhook Configuration

#### 1. Todoist Integration
```json
{
    "url": "http://192.168.0.63:8080/webhook/todoist",
    "headers": {
        "Content-Type": "application/json",
        "X-Signature": "YOUR_SIGNATURE"
    },
    "events": [
        "item:added",
        "item:completed",
        "item:updated"
    ],
    "priority_mapping": {
        "p1": "🔥 RED",
        "p2": "🟠 ORANGE",
        "p3": "🟡 YELLOW",
        "p4": "🟢 GREEN"
    }
}
```

#### 2. Email Integration
```json
{
    "url": "http://192.168.0.63:8080/webhook/email",
    "headers": {
        "Content-Type": "application/json"
    },
    "priority_triggers": {
        "urgent": ["urgent", "asap", "emergency"],
        "high": ["important", "priority"],
        "normal": []
    },
    "metadata_extraction": {
        "due_date": "regex patterns",
        "category": "keyword mapping",
        "priority": "subject line analysis"
    }
}
```

### Raw Data Schema

#### 1. Task Ingestion
```json
{
    "source": "string",  // email, todoist, manual
    "content": {
        "tasks": [{
            "content": "string",
            "urgent": boolean,
            "due_date": "YYYY-MM-DD",
            "category": "string",
            "metadata": {}
        }]
    },
    "priority": "string",  // urgent, normal
    "metadata": {
        "source_id": "string",
        "correlation_id": "string",
        "tags": ["string"]
    }
}
```

#### 2. Document Ingestion
```json
{
    "source": "document",
    "content": {
        "type": "string",  // email, letter, form
        "body": "string",
        "extracted_data": {
            "dates": ["string"],
            "actions": ["string"],
            "entities": ["string"]
        }
    },
    "metadata": {
        "doc_type": "string",
        "confidence": float,
        "requires_review": boolean
    }
}
```

### Processing Rules

#### 1. Priority Determination
```python
PRIORITY_RULES = {
    "RED": [
        "medical + overdue",
        "urgent + deadline",
        "tax + overdue",
        "vehicle + safety"
    ],
    "ORANGE": [
        "medical + upcoming",
        "tax + deadline",
        "vehicle + maintenance"
    ],
    "YELLOW": [
        "routine + scheduled",
        "maintenance + planned"
    ],
    "GREEN": [
        "general tasks",
        "future planning"
    ]
}
```

#### 2. Context Mapping
```python
CONTEXT_RULES = {
    "medical": {
        "keywords": ["doctor", "appointment", "screening"],
        "story_refs": ["Big Mickie's Hospital Adventure"],
        "voice_pattern": "concerned"
    },
    "vehicle": {
        "keywords": ["car", "repair", "maintenance"],
        "story_refs": ["Miss Pearl's Caddy Disaster"],
        "voice_pattern": "practical"
    },
    "financial": {
        "keywords": ["tax", "payment", "bill"],
        "story_refs": ["Big Mickie's Creative Accounting"],
        "voice_pattern": "serious"
    }
}
```

### Voice Pattern Configuration

#### 1. SSML Patterns
```json
{
    "emotions": {
        "concerned": "<amazon:emotion name=\"disappointed\" intensity=\"medium\"><prosody rate=\"95%\">$TEXT</prosody></amazon:emotion>",
        "urgent": "<amazon:emotion name=\"excited\" intensity=\"high\"><prosody rate=\"110%\" pitch=\"+10%\">$TEXT</prosody></amazon:emotion>",
        "caring": "<amazon:emotion name=\"happy\" intensity=\"low\"><prosody volume=\"soft\">$TEXT</prosody></amazon:emotion>"
    },
    "transitions": {
        "topic_change": "<break time=\"1s\"/><prosody pitch=\"+10%\" rate=\"110%\">$TEXT</prosody>",
        "story_intro": "<break time=\"500ms\"/><amazon:emotion name=\"excited\" intensity=\"medium\">$TEXT</amazon:emotion>"
    }
}
```

#### 2. Character Voice Rules
```json
{
    "base_voice": {
        "rate": "medium",
        "pitch": "medium-low",
        "style": "Boston accent"
    },
    "context_adjustments": {
        "medical": {
            "rate": "slower",
            "intensity": "higher",
            "style": "concerned"
        },
        "urgent": {
            "rate": "faster",
            "pitch": "higher",
            "style": "commanding"
        }
    }
}
```

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

## n8n Webhook Configuration

### 1. Webhook Node Setup
```json
{
    "node": "Webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": {
        "path": "ursula/tasks",
        "responseMode": "lastNode",
        "responseData": "allEntries",
        "options": {
            "allowUnauthorizedCerts": true,
            "bodyContentType": "json",
            "includeCookies": false,
            "timeout": 5000
        }
    }
}
```

### 2. Webhook Headers
```json
{
    "Content-Type": "application/json",
    "X-Source": "n8n",
    "X-Webhook-Key": "{{$env.WEBHOOK_SECRET}}",
    "Authorization": "Bearer {{$env.URSULA_API_TOKEN}}"
}
```

### 3. Webhook Body Parameters
```json
{
    "event_type": "{{ $json.eventType }}",
    "source": "n8n",
    "content": {
        "tasks": [
            {
                "id": "{{ $json.id }}",
                "content": "{{ $json.content }}",
                "description": "{{ $json.description }}",
                "due_date": "{{ $json.due_date }}",
                "priority": "{{ $json.priority }}",
                "labels": {{ $json.labels }},
                "docid": "{{ $json.docid }}"
            }
        ]
    },
    "metadata": {
        "workflow_id": "{{ $workflow.id }}",
        "run_id": "{{ $runIndex }}",
        "timestamp": "{{ $now }}",
        "source_system": "{{ $json.source }}",
        "document_refs": [
            {
                "id": "{{ $json.document.id }}",
                "type": "{{ $json.document.type }}",
                "url": "{{ $json.document.url }}"
            }
        ]
    },
    "priority": "{{ $json.priority == 'high' ? 'urgent' : 'normal' }}"
}
```

### 4. Document Attachment
```json
{
    "attachments": [
        {
            "type": "document",
            "binary_property": "data",
            "file_name": "{{ $json.document.name }}",
            "mime_type": "{{ $json.document.mime_type }}"
        }
    ],
    "include_document_content": true,
    "max_size_mb": 10,
    "allowed_types": ["pdf", "doc", "docx", "txt"]
}
```

### 5. Example n8n Workflow

```javascript
// 1. Webhook Trigger Node
{
    "webhook": {
        "path": "ursula/tasks",
        "method": "POST",
        "responseMode": "lastNode"
    }
}

// 2. Function Node (Data Transformation)
function processIncoming($input) {
    const item = $input.first();
    
    // Extract document if present
    let documentData = null;
    if (item.binary && item.binary.data) {
        documentData = {
            id: item.json.document?.id || generateId(),
            type: item.binary.data.mimeType,
            url: item.binary.data.fileName
        };
    }
    
    // Determine priority
    const priority = determinePriority(item.json);
    
    return {
        json: {
            event_type: "task_created",
            source: "n8n",
            content: {
                tasks: [{
                    id: item.json.id || generateId(),
                    content: item.json.content,
                    description: item.json.description,
                    due_date: formatDate(item.json.due_date),
                    priority: priority,
                    labels: item.json.labels || []
                }]
            },
            metadata: {
                workflow_id: $workflow.id,
                run_id: $runIndex,
                timestamp: new Date().toISOString(),
                document_refs: documentData ? [documentData] : []
            },
            priority: priority === "HIGH" ? "urgent" : "normal"
        }
    };
}

// 3. HTTP Request Node (Send to Ursula API)
{
    "url": "http://192.168.0.63:8080/ingest/raw",
    "method": "POST",
    "headers": {
        "Content-Type": "application/json",
        "X-Source": "n8n",
        "X-Webhook-Key": "{{$env.WEBHOOK_SECRET}}"
    },
    "bodyParametersUi": {
        "parameter": [
            {
                "name": "event_type",
                "value": "={{ $json.event_type }}"
            },
            {
                "name": "content",
                "value": "={{ $json.content }}"
            },
            {
                "name": "metadata",
                "value": "={{ $json.metadata }}"
            },
            {
                "name": "priority",
                "value": "={{ $json.priority }}"
            }
        ]
    }
}
```

### 6. Testing the Webhook

```bash
# Test with task data
curl -X POST http://192.168.0.63:8080/webhook/n8n \
-H "Content-Type: application/json" \
-H "X-Webhook-Key: your_secret_here" \
-d '{
    "content": "Medical appointment follow-up",
    "description": "Call Dr. Thompson about test results",
    "due_date": "2024-03-20",
    "priority": "high",
    "labels": ["medical", "urgent"],
    "document": {
        "id": "doc123",
        "type": "pdf",
        "url": "https://example.com/doc.pdf"
    }
}'

# Test with document upload
curl -X POST http://192.168.0.63:8080/webhook/n8n \
-H "Content-Type: multipart/form-data" \
-H "X-Webhook-Key: your_secret_here" \
-F "data={\"content\":\"Medical report review\"}" \
-F "document=@/path/to/report.pdf"
```
