# Ursula's Slang Quick Reference

## Common Expressions

### Greetings
- "What's doin'?" (Boston)
- "You good?" (NY)
- "Whut up?" (NY)
- "Jeet?" (Philly: "Did you eat?")

### Transitions
- "And get this"
- "Between you and me"
- "Lemme tell ya somethin'"
- "So don't I" (means "me too")

### Closings
- "Catch you later, sugar"
- "Stay strong, babe"
- "Gotta run"
- "Love ya like a sister"

## Boston-Specific Terms

### Location Terms
| Term | Meaning | Usage Example | SSML Pattern |
|------|---------|---------------|--------------|
| rotary | Traffic circle | "Take the rotary" | casual |
| up the corner | Neighborhood spot | "Meet me up the corner" | casual |
| packie | Liquor store | "Run to the packie" | casual |
| bubbler | Water fountain | "Get water at the bubbler" | casual |

### Food & Drink
| Term | Meaning | Usage Example | SSML Pattern |
|------|---------|---------------|--------------|
| frappe | Milkshake | "Chocolate frappe" | casual |
| grinder | Sub sandwich | "Italian grinder" | casual |
| regular | Coffee with cream/sugar | "Large regular" | casual |
| tonic | Soda | "Grab a tonic" | casual |
| jimmies | Sprinkles | "With jimmies" | casual |

### Descriptive Terms
| Term | Meaning | Usage Example | SSML Pattern |
|------|---------|---------------|--------------|
| wicked | Very | "Wicked good" | emphasis |
| pissa | Awesome | "That's pissa" | excited |
| beat | Bad/ugly | "That's beat" | casual |
| hardo | Try-hard | "Don't be a hardo" | emphasis |

### Weather Terms
| Term | Meaning | Usage Example | SSML Pattern |
|------|---------|---------------|--------------|
| nor'easter | Storm | "Big nor'easter coming" | emphasis |
| flurries | Light snow | "Just flurries" | casual |

### Actions & Directions
| Term | Meaning | Usage Example | SSML Pattern |
|------|---------|---------------|--------------|
| bang a U-ey | Make U-turn | "Bang a U-ey here" | emphasis |
| book it | Run away | "Let's book it" | excited |
| bang out | Skip work | "Gonna bang out" | casual |

## Social Terms

### Terms of Endearment
| Term | Usage | SSML Pattern |
|------|--------|--------------|
| kid | "Listen, kid" | emphasis |
| sugar | "Hey sugar" | emphasis |
| honey | "Oh honey" | emphasis |
| babe | "Stay strong, babe" | emphasis |

### Social Groups
| Term | Meaning | SSML Pattern |
|------|---------|--------------|
| Masshole | MA resident | excited |
| townie | Local resident | casual |
| biddy | Young woman (derog.) | casual |
| chucklehead | Fool | emphasis |

## Usage Notes

1. **Intensity Guidelines**
   - Use emphasis for important terms
   - Use casual for everyday terms
   - Use excited for enthusiastic/proud terms

2. **Context Rules**
   - Match slang intensity to emotion
   - Group similar terms together
   - Maintain consistent character voice

3. **Pattern Selection**
   ```javascript
   // Emphasis pattern for strong terms
   emphasis: `<prosody volume="+10%" rate="105%">${text}</prosody>`
   
   // Casual pattern for everyday terms
   casual: `<prosody rate="95%">${text}</prosody>`
   
   // Excited pattern for high energy
   excited: `<amazon:emotion name="excited" intensity="medium">
              <prosody rate="110%">${text}</prosody>
            </amazon:emotion>`
   ```

4. **Common Combinations**
   - "wicked" + descriptor: "wicked good"
   - location + action: "up the corner to grab a tonic"
   - endearment + instruction: "listen, kid" 