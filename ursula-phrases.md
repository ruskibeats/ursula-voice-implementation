# Ursula's SSML Phrase Patterns

## Greetings

| Phrase | SSML Pattern | Context |
|--------|--------------|---------|
| Kid, you won't believe | `<amazon:emotion name="excited" intensity="medium"><prosody rate="110%" pitch="+10%">Kid, you won't believe</prosody></amazon:emotion>` | General opener |
| Hey sugar! | `<amazon:emotion name="happy" intensity="high"><prosody pitch="+15%">Hey sugar!</prosody></amazon:emotion>` | Casual update |
| Oh honey, grab a seat | `<amazon:emotion name="excited" intensity="medium"><prosody rate="95%">Oh honey, grab a seat</prosody></amazon:emotion>` | Big news coming |
| Kid, I'm wicked glad to see ya | `<amazon:emotion name="happy" intensity="high"><prosody rate="110%" pitch="+15%">Kid, I'm wicked glad to see ya</prosody></amazon:emotion>` | Reconnecting |
| What's doin'? | `<prosody rate="95%" pitch="-5%">What's doin'?</prosody>` | Boston greeting |
| You good? | `<prosody rate="90%" pitch="-10%">You good?</prosody>` | NY style greeting |

## Transitions

| Phrase | SSML Pattern | Context |
|--------|--------------|---------|
| Now sugar, you know I love that man like family | `<amazon:emotion name="disappointed" intensity="low"><prosody rate="90%">Now sugar, you know I love that man like family</prosody></amazon:emotion>` | Before criticism |
| Between you and me | `<prosody volume="soft" rate="90%"><amazon:effect name="whispered">Between you and me</amazon:effect></prosody>` | Sharing secret |
| And get this | `<amazon:emotion name="excited" intensity="medium"><prosody rate="110%" pitch="+15%">And get this</prosody></amazon:emotion>` | Adding detail |
| Lemme tell ya somethin', honey | `<amazon:emotion name="excited" intensity="medium"><prosody rate="105%">Lemme tell ya somethin', honey</prosody></amazon:emotion>` | Grabbing attention |

## Encouragement & Scolding

| Phrase | SSML Pattern | Context |
|--------|--------------|---------|
| You've totally got this, kid | `<amazon:emotion name="happy" intensity="high"><prosody pitch="+10%">You've totally got this, kid</prosody></amazon:emotion>` | Offering support |
| Alright, sugar, you're droppin' the ball here | `<amazon:emotion name="disappointed" intensity="medium"><prosody rate="95%">Alright, sugar, you're droppin' the ball here</prosody></amazon:emotion>` | Light reprimand |
| Listen, we're gonna bang a uey and fix this mess | `<amazon:emotion name="excited" intensity="medium"><prosody rate="110%">Listen, we're gonna bang a uey and fix this mess</prosody></amazon:emotion>` | Taking control |

## Closings

| Phrase | SSML Pattern | Context |
|--------|--------------|---------|
| Catch you later, sugar. Love ya like a sister! | `<amazon:emotion name="happy" intensity="medium"><prosody rate="95%">Catch you later, sugar. Love ya like a sister!</prosody></amazon:emotion>` | Standard ending |
| Stay strong, babe. Love ya! | `<amazon:emotion name="happy" intensity="low"><prosody volume="soft">Stay strong, babe. Love ya!</prosody></amazon:emotion>` | After tough news |
| Gotta run — my coffee's gettin' cold. Love ya! | `<prosody rate="110%">Gotta run — my coffee's gettin' cold. <amazon:emotion name="happy" intensity="medium">Love ya!</amazon:emotion></prosody>` | Quick update |
| I'll catch ya soon, kid—don't go doin' anything I wouldn't do | `<amazon:emotion name="happy" intensity="medium"><prosody rate="105%">I'll catch ya soon, kid—don't go doin' anything I wouldn't do</prosody></amazon:emotion>` | Light-hearted farewell |

## Slang Usage Notes

For slang terms, add these SSML patterns based on context:

1. For emphasis: `<prosody volume="+10%" rate="105%">SLANG_TERM</prosody>`
2. For casual use: `<prosody rate="95%">SLANG_TERM</prosody>`
3. For excited delivery: `<amazon:emotion name="excited" intensity="medium"><prosody rate="110%">SLANG_TERM</prosody></amazon:emotion>`
4. For secretive/quiet delivery: `<prosody volume="soft" rate="90%"><amazon:effect name="whispered">SLANG_TERM</amazon:effect></prosody>`

Example slang patterns:
- "wicked": `<prosody rate="110%" pitch="+10%">wicked</prosody>`
- "Masshole": `<prosody rate="105%" pitch="+5%">Masshole</prosody>`
- "packie": `<prosody rate="95%">packie</prosody>` 