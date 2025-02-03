# Ursula API Documentation

## Base URL
```bash
http://192.168.0.63:8080
```

## Core Relationship Endpoints

### Get Person Relationship
```bash
GET /api/ursula/memory/relationships/{person_name}

# Example Response:
{
    "id": 10,
    "person_name": "Russ",
    "relationship_type": "primary_client",
    "dynamic": "protective_mentor",
    "special_notes": "Former Wall Street colleague's son, needs constant medical supervision",
    "interaction_history": [{
        "date": "2024-02-01",
        "type": "medical_reminder",
        "success": 0.8
    }],
    "last_interaction": null
}
```

### Get Romantic Relationship
```bash
GET /api/ursula/memory/romance/{name}

# Example Response:
{
    "id": 4,
    "name": "Viktor Petrov",
    "era": "brighton_beach",
    "relationship_type": "the_one_that_got_away",
    "status": "complicated",
    "story": "Never married him, should have. The one who understood both sides of her - street and sophistication",
    "special_notes": "Monthly chess games, occasional lovers",
    "locations": ["Tatiana Restaurant", "Brighton Beach Boardwalk"],
    "interaction_history": [{
        "date": "2024-01-15",
        "type": "chess_night",
        "success": 0.9
    }]
}
```

## Story Endpoints

### Get Stories by Category
```bash
GET /api/ursula/memory/stories/{category}

# Example Response:
[{
    "id": 7,
    "title": "The Goldman Sachs Incident",
    "category": "medical_warning",
    "location": "Trading Floor",
    "characters": ["Big Mickie", "Dr. Thompson"],
    "content": "Big Mickie ignored his blood pressure meds, collapsed during a big trade",
    "mood": "cautionary",
    "times_told": 5,
    "last_told": null,
    "success_rating": null
}]
```

### Get Romantic Stories
```bash
GET /api/ursula/memory/romance/stories/{category}

# Example Response:
[{
    "id": 4,
    "title": "Chess and Champagne",
    "category": "passionate",
    "location": "Brighton Beach",
    "characters": ["Viktor Petrov", "The Russian Choir"],
    "content": "Viktor taught her chess while drinking champagne. She taught him about options trading. Love bloomed.",
    "mood": "nostalgic",
    "times_told": 3,
    "last_told": null,
    "success_rating": null
}]
```

## Pattern Endpoints

### Get Emotional Patterns
```bash
GET /api/ursula/patterns/emotion

# Example Response:
[{
    "pattern_type": "emotion",
    "pattern_name": "caring",
    "ssml_pattern": "<amazon:emotion name=\"happy\" intensity=\"low\"><prosody volume=\"soft\" rate=\"95%\">$TEXT</prosody></amazon:emotion>",
    "description": "For empathetic moments"
}, {
    "pattern_type": "emotion",
    "pattern_name": "confident",
    "ssml_pattern": "<amazon:emotion name=\"excited\" intensity=\"medium\"><prosody rate=\"+5%\" pitch=\"+10%\">$TEXT</prosody></amazon:emotion>",
    "description": "For authoritative statements"
}]
```

## Template Endpoints

### Get Response Templates
```bash
GET /api/ursula/templates/{template_type}

# Available template_types:
- medical_urgent
- general_update
```

### Get Voicemail Templates
```bash
GET /api/ursula/voicemail/templates/{template_name}

# Available template_names:
- medical_urgent
- general_update
```

## Memory Update Endpoints

### Store New Memory
```bash
POST /api/ursula/memory/store
Content-Type: application/json

{
    "category": "medical_emergency",
    "content": {
        "patient": "Russ",
        "situation": "Missed medication",
        "location": "Mass General"
    },
    "context": "urgent_care"
}
```

### Update Story Stats
```bash
POST /api/ursula/stories/update
Content-Type: application/json

{
    "story_id": 1,
    "times_told": 5,
    "success_rating": 0.9
}
```

### Track Pattern Response
```bash
POST /api/ursula/patterns/response
Content-Type: application/json

{
    "pattern_id": 1,
    "response_type": "positive"  // or "neutral", "negative"
}
```

## SSML Build Endpoint

### Build SSML Response
```bash
POST /api/ursula/ssml/build
Content-Type: application/json

{
    "text": "Sugar, this is urgent",
    "pattern_type": "emotion",
    "pattern_name": "caring"
}

# Response:
{
    "ssml": "<amazon:emotion name=\"happy\" intensity=\"low\"><prosody volume=\"soft\" rate=\"95%\">Sugar, this is urgent</prosody></amazon:emotion>"
}
```

## Error Responses
```json
{
    "detail": "Error message description"
}
```

Status Codes:
- 200: Success
- 404: Not Found
- 500: Internal Server Error 