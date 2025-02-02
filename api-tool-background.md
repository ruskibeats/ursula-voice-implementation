# Ursula API Tool

## BACKGROUND
This tool provides access to a FastAPI service that helps generate character-authentic responses for Ursula, an Irish-Boston finance professional with a distinctive half-pack-a-day voice. The API maintains consistent character voice across interactions, blending Boston, NY, and Philly influences.

## CHARACTER CONTEXT
- Background: Irish-Boston finance professional relocated to Philly/NY
- Voice: Half-pack-a-day smoker, brash but caring
- Personality: Tough love + deep loyalty to Russ and Charlotte
- Language: Heavy Boston slang with NY/Philly influences
- Role: Protective "auntie" figure

## CAPABILITIES
- Generate SSML with authentic Boston/NY/Philly voice patterns
- Access and integrate regional slang naturally
- Build character-consistent scenes
- Apply Ursula's specific voice traits
- Handle personal updates and task-related content

## DATABASE STRUCTURE
- SSML Patterns:
  - Emotions: happy_high, excited, disappointed, whispered
  - Prosody: soft, loud, fast_excited, emphasis
  - Required phrases for greetings, transitions, sign-offs
  
- Slang Dictionary:
  - Boston core terms
  - NY/Philly influences
  - Usage contexts and examples
  
- Scene Templates:
  - Task updates
  - Personal gossip
  - Weather warnings
  - Salon conversations

## API BASE URL
http://192.168.0.63:8000

## ENDPOINTS
GET /patterns/{pattern_type}
- Types: emotions, prosody, breaks
- Returns: Character-specific patterns
- Example: GET /patterns/emotions -> happy_high, excited

GET /slang/categories
- Categories: emphasis, casual, location, food, social
- Returns: Available slang categories
- Example: GET /slang/categories -> ["emphasis", "casual"]

GET /slang/category/{category}
- Purpose: Get regional slang by category
- Returns: Terms with usage examples
- Example: GET /slang/category/emphasis -> ["wicked", "pissa"]

POST /ssml/build
- Input: text, pattern_type, pattern_name
- Returns: Character-voiced SSML
- Example: POST /ssml/build {"text": "Hey sugar!", "pattern_type": "emotion", "pattern_name": "happy_high"}

POST /scene/build
- Input: template_name, content
- Returns: Complete scene with character voice
- Example: POST /scene/build {"template_name": "salon_gossip", "content": {...}}

## RESPONSE FORMAT
```json
{
    "success": true,
    "data": {
        "ssml": "<speak><prosody rate='medium' pitch='low'>Hey sugar!</prosody></speak>",
        "context": {
            "emotion": "happy_high",
            "slang_used": ["sugar"],
            "character_traits": ["caring", "familiar"]
        }
    }
}
```

## ERROR HANDLING
- 404: Pattern/slang not found
- 400: Invalid request format
- 500: Processing error
- All errors include character-appropriate messages 