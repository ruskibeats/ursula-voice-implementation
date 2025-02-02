# Ursula Voice Implementation

A FastAPI-based voice personality system that manages Ursula's character voice, SSML patterns, and interaction memory. The system tracks pattern effectiveness and adapts responses based on success rates.

## Features

### Voice Pattern Management
- SSML pattern library with emotions, prosody, and effects
- Boston/NY/Philly regional slang integration
- Dynamic pattern success tracking
- Automatic adaptation based on response effectiveness

### Memory System
- Relationship tracking with interaction history
- Story database with categorization
- Pattern effectiveness metrics
- Success rate calculation for different approaches

### API Endpoints

#### Pattern Management
```bash
# Get patterns by type
GET /api/ursula/patterns/{pattern_type}

# Get pattern statistics
GET /api/ursula/stats/patterns

# Track pattern response
POST /api/ursula/patterns/response
{
    "pattern_id": 1,
    "response_type": "positive"  # or "neutral"/"negative"
}
```

#### Memory Management
```bash
# Get relationship data
GET /api/ursula/memory/relationships/{person_name}

# Store new memory
POST /api/ursula/memory/store
{
    "category": "medical",
    "content": { ... },
    "context": "concerned_reminder"
}

# Get recent memories
GET /api/ursula/memory/recent/{category}
```

#### Story Management
```bash
# Get stories by category
GET /api/ursula/memory/stories/{category}

# Get favorite stories
GET /api/ursula/stories/favorite

# Update story stats
POST /api/ursula/stories/update
{
    "story_id": 1,
    "times_told": 5,
    "success_rating": 0.9
}
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ruskibeats/ursula-voice-implementation.git
cd ursula-voice-implementation
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize database:
```bash
python3 init_db.py
```

5. Start the server:
```bash
uvicorn ursula_api:app --host 0.0.0.0 --port 8080
```

## Database Schema

### Core Tables
- `core_identity`: Base personality traits
- `relationships`: Person relationships and interaction history
- `stories`: Story database with success metrics
- `interaction_patterns`: SSML patterns with effectiveness tracking
- `memory_updates`: Interaction memory storage

### Views
- `recent_successful_patterns`: Patterns with success rate > 0.7
- `favorite_stories`: Stories with success rating > 0.8

## Pattern Success Tracking

The system tracks pattern effectiveness through:
1. Response tracking (positive/neutral/negative)
2. Success rate calculation:
   ```
   success_rate = (positive_responses * 1.0 + neutral_responses * 0.5) / total_responses
   ```
3. Pattern adaptation based on success rates
4. Automatic selection of most effective patterns

## SSML Pattern Examples

### Emotional Patterns
```xml
<!-- Excited greeting -->
<amazon:emotion name="excited" intensity="medium">
    <prosody rate="110%" pitch="+10%">
        Kid, you won't believe what happened!
    </prosody>
</amazon:emotion>

<!-- Concerned reminder -->
<amazon:emotion name="concerned" intensity="medium">
    Sugar, that medical appointment is {days} days overdue.
    We can't have another Big Mickie situation!
</amazon:emotion>
```

### Regional Slang Integration
```xml
<!-- Boston style -->
<prosody rate="95%" pitch="-5%">
    What's doin'?
</prosody>

<!-- NY influence -->
<prosody rate="90%" pitch="-10%">
    You good?
</prosody>
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
