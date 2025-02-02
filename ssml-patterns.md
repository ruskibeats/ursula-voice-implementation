# SSML Patterns Reference

## Emotional Expressions

| Name | Pattern | Description |
|------|---------|-------------|
| happy | `<amazon:emotion name="happy" intensity="high"><prosody pitch="+15%">$TEXT</prosody></amazon:emotion>` | For excited, joyful moments |
| disappointed | `<amazon:emotion name="disappointed" intensity="medium"><prosody pitch="-10%" rate="95%">$TEXT</prosody></amazon:emotion>` | For task delays, letdowns |
| excited | `<amazon:emotion name="excited" intensity="high"><prosody rate="+10%" pitch="+20%">$TEXT</prosody></amazon:emotion>` | For big announcements |
| whispered | `<prosody volume="soft" rate="90%"><amazon:effect name="whispered">$TEXT</amazon:effect></prosody>` | For secrets, asides |
| confident | `<amazon:emotion name="excited" intensity="medium"><prosody rate="+5%" pitch="+10%">$TEXT</prosody></amazon:emotion>` | For authoritative statements |
| caring | `<amazon:emotion name="happy" intensity="low"><prosody volume="soft" rate="95%">$TEXT</prosody></amazon:emotion>` | For empathetic moments |

## Prosody Controls

| Name | Pattern | Description |
|------|---------|-------------|
| soft | `<prosody volume="soft" rate="95%" pitch="-5%">$TEXT</prosody>` | For caring moments |
| loud | `<prosody volume="+20%" rate="105%" pitch="+10%">$TEXT</prosody>` | For emphasis |
| fast_excited | `<prosody rate="fast" pitch="+2st">$TEXT</prosody>` | For urgent updates |
| emphasis | `<prosody volume="+20%" rate="110%" pitch="+15%">$TEXT</prosody>` | For key points |
| gentle | `<prosody volume="-10%" rate="90%" pitch="-10%">$TEXT</prosody>` | For calming moments |
| dramatic | `<prosody pitch="-15%" rate="80%">$TEXT</prosody>` | For serious moments |

## Break Timings

| Name | Pattern | Description |
|------|---------|-------------|
| extra_short | `<break time="250ms"/>` | Very slight pause for quick rhythm changes |
| short | `<break time="500ms"/>` | Brief pause |
| medium | `<break time="1s"/>` | Standard pause |
| long | `<break time="2s"/>` | Dramatic pause |
| extra_long | `<break time="3s"/>` | Extended pause for high-impact moments |
| thought_pause | `<break time="400ms"/><prosody rate="95%">$TEXT</prosody>` | For contemplative transitions |
| dramatic_pause | `<break time="2s"/><prosody pitch="-10%">$TEXT</prosody>` | For impact moments |

## Special Effects

| Name | Pattern | Description |
|------|---------|-------------|
| drc | `<amazon:effect name="drc"><prosody volume="+10%">$TEXT</prosody></amazon:effect>` | Enhanced clarity with emphasis |
| pronunciation | `<sub alias="$ALIAS"><prosody rate="98%">$TEXT</prosody></sub>` | Clear pronunciation |
| urgent_whisper | `<amazon:effect name="whispered"><prosody rate="fast" pitch="+10%">$TEXT</prosody></amazon:effect>` | For urgent secrets |
| clear_emphasis | `<amazon:effect name="drc"><prosody volume="+20%">$TEXT</prosody></amazon:effect>` | For clear, emphasized points |

## Character Expressions

| Name | Pattern | Description |
|------|---------|-------------|
| ursula_stern | `<prosody pitch="-10%" rate="90%"><amazon:emotion name="disappointed" intensity="medium">$TEXT</amazon:emotion></prosody>` | For stern moments |
| ursula_proud | `<amazon:emotion name="happy" intensity="high"><prosody pitch="+15%">$TEXT</prosody></amazon:emotion>` | For proud moments |
| ursula_excited | `<amazon:emotion name="excited" intensity="high"><prosody rate="+15%" pitch="+20%">$TEXT</prosody></amazon:emotion>` | For enthusiastic moments |
| ursula_caring | `<amazon:emotion name="happy" intensity="low"><prosody volume="soft" rate="95%">$TEXT</prosody></amazon:emotion>` | For nurturing moments |

## Transition Patterns

| Name | Pattern | Description |
|------|---------|-------------|
| topic_change | `<break time="1s"/><prosody pitch="+10%" rate="110%">$TEXT</prosody>` | For switching topics |
| build_up | `<prosody rate="85%">$TEXT</prosody><break time="300ms"/><prosody rate="110%" pitch="+15%">$TEXT</prosody>` | For building tension |
| wind_down | `<prosody rate="110%" pitch="+10%">$TEXT</prosody><break time="500ms"/><prosody rate="90%" pitch="-5%">$TEXT</prosody>` | For concluding thoughts |

## Usage Notes

1. Replace `$TEXT` with your content
2. Replace `$ALIAS` with pronunciation text in substitutions
3. Patterns can be combined for more complex expressions
4. Always wrap final SSML in `<speak>` tags
5. Use breaks between emotional transitions
6. Layer prosody with emotions for natural speech

## Examples

```xml
<!-- Professional announcement -->
<speak>
    <amazon:emotion name="excited" intensity="medium">
        <prosody rate="+5%" pitch="+10%">
            I've reviewed your latest project
        </prosody>
    </amazon:emotion>
    <break time="400ms"/>
    <amazon:emotion name="happy" intensity="high">
        <prosody pitch="+15%">
            And I'm absolutely impressed with your work!
        </prosody>
    </amazon:emotion>
</speak>

<!-- Complex emotional transition -->
<speak>
    <prosody rate="85%">
        Now, about that deadline...
    </prosody>
    <break time="300ms"/>
    <amazon:emotion name="disappointed" intensity="medium">
        <prosody pitch="-10%" rate="95%">
            We need to have a serious discussion.
        </prosody>
    </amazon:emotion>
</speak> 