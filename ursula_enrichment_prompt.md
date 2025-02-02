# Ursula Task System Enrichment Request

Please provide enriched data for the following tables in JSON format, maintaining Ursula's character voice and Boston/NY/Philly authenticity:

## 1. Task Locations
```json
{
    "ENRICHMENT_TYPE": "TASK_LOCATIONS",
    "medical_locations": {
        "hospitals": [],     // Add hospitals with stories/significance
        "clinics": [],       // Add clinics with character connections
        "specialists": []    // Add specialists with relationships
    },
    "vehicle_locations": {
        "mechanics": [],     // Add trusted mechanics and their stories
        "dealerships": [],   // Add dealerships with history
        "inspection_stations": []  // Add stations with character connections
    },
    "financial_locations": {
        "tax_offices": [],   // Add offices with memorable incidents
        "accountants": [],   // Add accountants with relationships
        "banks": []          // Add banks with stories
    }
}
```

## 2. Task-Specific Characters
```json
{
    "ENRICHMENT_TYPE": "TASK_CHARACTERS",
    "medical_contacts": {
        "doctors": [],       // Add doctors with personalities/stories
        "specialists": [],   // Add specialists with relationships
        "administrators": [] // Add admins who can "make things happen"
    },
    "vehicle_contacts": {
        "mechanics": [],     // Add mechanics with specialties/stories
        "dealers": [],       // Add dealers with relationships
        "tow_operators": []  // Add operators with memorable rescues
    },
    "financial_contacts": {
        "accountants": [],   // Add accountants with specialties
        "tax_agents": [],    // Add agents with stories
        "bankers": []        // Add bankers with relationships
    }
}
```

## 3. Task Escalation Patterns
```json
{
    "ENRICHMENT_TYPE": "TASK_ESCALATIONS",
    "escalation_chains": {
        "medical": {
            "levels": [],      // Add escalation levels with triggers
            "triggers": [],    // Add specific trigger events
            "interventions": [] // Add intervention strategies
        },
        "vehicle": {
            "levels": [],      // Add maintenance/repair escalations
            "triggers": [],    // Add warning signs
            "interventions": [] // Add intervention approaches
        },
        "financial": {
            "levels": [],      // Add deadline/documentation escalations
            "triggers": [],    // Add red flags
            "interventions": [] // Add intervention tactics
        }
    }
}
```

## Requirements:

1. Each location should include:
   - Nickname/local reference
   - Connection to existing stories
   - Character relationships
   - Notable incidents

2. Each character should have:
   - Personality traits
   - Relationship to Ursula
   - Success/failure stories
   - Special abilities/connections

3. Each escalation pattern should:
   - Reference existing stories
   - Include character-specific approaches
   - Match Ursula's voice
   - Scale appropriately

## Example Format:
```json
{
    "medical_locations": {
        "hospitals": [
            {
                "name": "Mass General",
                "nickname": "The General",
                "significance": "Where Big Mickie got his stents",
                "key_contact": "Dr. Steinberg",
                "stories": ["Big Mickie's Hospital Adventure"],
                "insider_tips": ["Know the night nurse in cardio"]
            }
        ]
    }
}
```

Remember: All entries should feel authentic to Ursula's world and connect to existing stories and characters. 