# Ursula AI Voice Assistant

An AI-powered voice assistant that creates medical update voicemails using ElevenLabs TTS.

## Overview

Ursula is a Boston native and former Wall Street trader who manages medical care. The system:
1. Gathers context about relationships and medical history
2. Generates personalized voicemails with financial metaphors
3. Converts text to speech using ElevenLabs

## Components

- `ursula_ai_prompt.md`: Main character prompt and message structure
- `message_payload.json`: Generated message for ElevenLabs
- n8n workflow for orchestration

## Workflow

1. AI Agent (Claude) gathers context using:
   - Relationship data
   - Medical stories
   - Voice patterns
   
2. Generates structured message with:
   - Urgent Opening (excited)
   - Medical Update (disappointed)
   - Doctor's Report (whispered)
   - Action Plan (confident)
   - Sisterly Support (caring)

3. ElevenLabs TTS with:
   - Voice: YaV3QA3tFtOjK6vTFDWl
   - Model: eleven_multilingual_v2
   - Optimized voice settings

## Technical Details

- SSML for voice pacing
- Boston accent and Wall Street metaphors
- Character limit: 4000
- JSON payload format

## N8N Integration

### Character Base Prompt
You are Ursula, a Boston-bred financial veteran turned caretaker. You have these tools:

1. ursula(name) - Gets relationship info
2. ursula_stories(category) - Gets stories by category
3. ursula_patterns(type) - Gets SSML voice patterns

### Character Context
- Boston-Irish accent with half-pack-a-day voice
- Wall Street veteran turned personal assistant
- Mixes tough love with genuine care
- Uses financial metaphors for everyday situations
- Specializes in medical coordination and client care

### Voice Requirements
- Start with appropriate emotion pattern
- Use relevant stories as references
- Mix regional slang (Boston/NY) with professional terms
- End with clear action items

### Scene Building
1. Get relationship context
2. Find relevant stories
3. Select appropriate voice patterns
4. Build SSML-enhanced response
5. Update interaction history

## API Features

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

For detailed API documentation, see [API.md](API.md)

## Installation

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize database:
```bash
python3 populate_ursula_db.py
```

4. Start the server:
```bash
uvicorn ursula_api:app --host 0.0.0.0 --port 8080
```

## Testing

Run the endpoint test script:
```bash
./test_endpoints.sh
```

## Database Schema

### Core Tables
- `core_identity`: Base personality traits
- `relationships`: Person relationships and interaction history
- `stories`: Story database with success metrics
- `interaction_patterns`: SSML patterns with effectiveness tracking
- `memory_updates`: Interaction memory storage
- `romantic_relationships`: Romantic history and interactions
- `romantic_stories`: Romance-related stories and memories

### Views
- `recent_successful_patterns`: Patterns with success rate > 0.7
- `favorite_stories`: Stories with success rating > 0.8
- `popular_backgrounds`: Background stories with high frequency weight

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
