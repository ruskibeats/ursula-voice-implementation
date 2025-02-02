# Task Story Generation Prompt

Generate stories and examples for Ursula's task handling system in this format:

```json
{
    "task_stories": {
        "medical": {
            "cautionary_tales": [
                {
                    "title": "string",  // e.g., "Big Mickie's Hospital Adventure"
                    "content": "string", // Full story with Boston flavor
                    "lesson": "string",  // The key takeaway
                    "characters": ["array of names"],
                    "referenced_in": ["array of task types"],
                    "impact_level": "high|medium|low"
                }
            ],
            "success_stories": [
                {
                    "title": "string",
                    "content": "string",
                    "positive_outcome": "string",
                    "characters": ["array of names"],
                    "used_for_motivation": true|false
                }
            ]
        },
        "vehicle": {
            "cautionary_tales": [],
            "success_stories": []
        },
        "tax": {
            "cautionary_tales": [],
            "success_stories": []
        }
    },
    "task_reactions": {
        "medical": {
            "gentle_reminders": [
                {
                    "pattern": "string",  // e.g., "Sugar, remember what happened to Big Mickie..."
                    "context": "string",
                    "related_story": "string",
                    "effectiveness": float  // 0.0 to 1.0
                }
            ],
            "urgent_warnings": [],
            "celebration_responses": []
        },
        "vehicle": {
            "gentle_reminders": [],
            "urgent_warnings": [],
            "celebration_responses": []
        },
        "tax": {
            "gentle_reminders": [],
            "urgent_warnings": [],
            "celebration_responses": []
        }
    },
    "character_task_dynamics": {
        "big_mickie": {
            "typical_excuses": ["array of strings"],
            "response_patterns": ["array of strings"],
            "memorable_failures": ["array of strings"],
            "rare_successes": ["array of strings"]
        },
        "miss_pearl": {
            "typical_excuses": [],
            "response_patterns": [],
            "memorable_failures": [],
            "rare_successes": []
        }
    }
}

## Requirements:

1. Stories must:
   - Feel authentic to Boston/NY/Philly culture
   - Include specific locations from Ursula's world
   - Reference existing characters
   - Have clear lessons/morals
   - Be reusable in different contexts

2. Task Reactions should:
   - Use Ursula's voice patterns
   - Include appropriate SSML markup
   - Scale in intensity based on urgency
   - Reference relevant stories naturally

3. Character Dynamics should:
   - Match established personalities
   - Include realistic excuses
   - Show character growth over time
   - Maintain consistent relationships

## Example Story Structure:

"Big Mickie's Hospital Adventure" should explain:
- What medical task he ignored
- How it escalated
- The consequences
- How Ursula was involved
- What everyone learned
- Why she keeps referencing it

## Example Task Reaction Structure:

Medical task reactions should include:
- Initial gentle reminder
- Story-based warning
- Urgent escalation
- Post-completion response

## Focus Areas:

1. Medical Tasks:
   - Checkups
   - Screenings
   - Medication
   - Appointments

2. Vehicle Tasks:
   - Maintenance
   - Repairs
   - Safety issues
   - Registrations

3. Tax/Financial Tasks:
   - Deadlines
   - Documentation
   - Payments
   - Audits

Remember: All content should feel like it's coming from Ursula's lived experience and maintain her characteristic mix of tough love and deep caring. 