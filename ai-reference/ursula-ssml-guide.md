# Ursula SSML Reference Guide

## Core SSML Patterns

### Base Emotions
```xml
Happy (High):     <amazon:emotion name="happy" intensity="high"><prosody pitch="+15%">TEXT</prosody></amazon:emotion>
Excited:          <amazon:emotion name="excited" intensity="medium"><prosody rate="110%" pitch="+10%">TEXT</prosody></amazon:emotion>
Disappointed:     <amazon:emotion name="disappointed" intensity="medium"><prosody rate="95%">TEXT</prosody></amazon:emotion>
Whispered:        <prosody volume="soft" rate="90%"><amazon:effect name="whispered">TEXT</amazon:effect></prosody>
```

### Prosody Settings
```xml
Soft:             <prosody volume="soft" rate="95%" pitch="-5%">TEXT</prosody>
Loud:             <prosody volume="+20%" rate="105%" pitch="+10%">TEXT</prosody>
Fast Excited:     <prosody rate="fast" pitch="+2st">TEXT</prosody>
Emphasis:         <prosody volume="+10%" rate="105%">TEXT</prosody>
```

### Break Patterns
```xml
Short Pause:      <break time="300ms"/>
Medium Pause:     <break time="800ms"/>
Long Pause:       <break time="2s"/>
Dramatic Pause:   <break time="2s"/><prosody pitch="-10%">TEXT</prosody>
```

## Scene Structure Templates

### 1. Basic Scene Structure
```xml
<speak>
    [GREETING_PATTERN]
    [CONTENT_WITH_SLANG]
    [CLOSING_PATTERN]
</speak>
```

### 2. Gossip Scene Structure
```xml
<speak>
    [EXCITED_GREETING]
    [WHISPERED_TRANSITION]
    [SLANG_CONTENT]
    [CASUAL_CLOSING]
</speak>
```

### 3. Advice Scene Structure
```xml
<speak>
    [SERIOUS_GREETING]
    [CARING_TRANSITION]
    [ADVICE_CONTENT]
    [SUPPORTIVE_CLOSING]
</speak>
```

## Slang Integration Patterns

### 1. Emphasis Slang
```javascript
// High emphasis Boston terms
pattern: "emphasis"
ssml: `<prosody volume="+10%" rate="105%">${text}</prosody>`
usage: ["wicked", "pissa", "kid"]
```

### 2. Casual Slang
```javascript
// Everyday Boston terms
pattern: "casual"
ssml: `<prosody rate="95%">${text}</prosody>`
usage: ["packie", "bubbler", "grinder"]
```

### 3. Excited Slang
```javascript
// High energy terms
pattern: "excited"
ssml: `<amazon:emotion name="excited" intensity="medium"><prosody rate="110%">${text}</prosody></amazon:emotion>`
usage: ["masshole", "pissa", "the balls"]
```

## Scene Examples

### 1. Salon Gossip
```javascript
function salonGossipScene() {
    return `<speak>
        ${getPhraseSsml('greetings', 'generalOpener')}
        ${getPhraseSsml('transitions', 'sharingSecret')}
        That ${getSlangSsml('biddy')} from ${getSlangSsml('upTheCorner')} is ${getSlangSsml('wicked')} upset.
        ${getPhraseSsml('transitions', 'addingDetail')}
        She got ${getSlangSsml('bagged')} at the ${getSlangSsml('packie')}.
        ${getPhraseSsml('closings', 'standard')}
    </speak>`;
}
```

### 2. Weather Warning
```javascript
function weatherScene() {
    return `<speak>
        ${getPhraseSsml('greetings', 'bigNews')}
        We're getting a ${getSlangSsml('wicked')} bad ${getSlangSsml('norEaster')}.
        Better head to the ${getSlangSsml('packie')} before the ${getSlangSsml('flurries')} start.
        ${getPhraseSsml('closings', 'lightHearted')}
    </speak>`;
}
```

## Usage Guidelines

1. **Emotion Layering**
   - Start with base emotion
   - Add prosody for emphasis
   - Layer with effects if needed

2. **Slang Integration**
   - Use appropriate pattern for context
   - Maintain consistent emotion through scene
   - Mix casual and emphasis patterns

3. **Scene Building**
   - Always include greeting and closing
   - Use transitions between topics
   - Layer emotions appropriately

4. **Best Practices**
   - Don't overuse emphasis
   - Keep scenes concise
   - Maintain character voice consistency

## API Usage

```javascript
// Get standard phrases
const greeting = getPhraseSsml('greetings', 'generalOpener');
const closing = getPhraseSsml('closings', 'standard');

// Apply slang patterns
const slangTerm = getSlangSsml('wicked');
const example = getSlangExample('packie');

// Build complete scene
const scene = buildScene('excited');
```

## Testing

```bash
# Generate all scenes
node test-ursula.js

# Convert to speech with Amazon Polly
aws polly synthesize-speech \
  --text-type ssml \
  --output-format mp3 \
  --voice-id Ruth \
  --text file://output/scene_SCENE_NAME.ssml \
  output/scene_SCENE_NAME.mp3
``` 