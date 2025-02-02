const ssmlPatterns = {
    emotions: {
        happy: {
            pattern: '<amazon:emotion name="happy" intensity="high"><prosody pitch="+15%">$TEXT</prosody></amazon:emotion>',
            description: 'For excited, joyful moments'
        },
        disappointed: {
            pattern: '<amazon:emotion name="disappointed" intensity="medium"><prosody pitch="-10%" rate="95%">$TEXT</prosody></amazon:emotion>',
            description: 'For task delays, letdowns'
        },
        excited: {
            pattern: '<amazon:emotion name="excited" intensity="high"><prosody rate="+10%" pitch="+20%">$TEXT</prosody></amazon:emotion>',
            description: 'For big announcements'
        },
        whispered: {
            pattern: '<prosody volume="soft" rate="90%"><amazon:effect name="whispered">$TEXT</amazon:effect></prosody>',
            description: 'For secrets, asides'
        },
        confident: {
            pattern: '<amazon:emotion name="excited" intensity="medium"><prosody rate="+5%" pitch="+10%">$TEXT</prosody></amazon:emotion>',
            description: 'For authoritative statements'
        },
        caring: {
            pattern: '<amazon:emotion name="happy" intensity="low"><prosody volume="soft" rate="95%">$TEXT</prosody></amazon:emotion>',
            description: 'For empathetic moments'
        }
    },
    prosody: {
        soft: {
            pattern: '<prosody volume="soft" rate="95%" pitch="-5%">$TEXT</prosody>',
            description: 'For caring moments'
        },
        loud: {
            pattern: '<prosody volume="+20%" rate="105%" pitch="+10%">$TEXT</prosody>',
            description: 'For emphasis'
        },
        fast_excited: {
            pattern: '<prosody rate="fast" pitch="+2st">$TEXT</prosody>',
            description: 'For urgent updates'
        },
        emphasis: {
            pattern: '<prosody volume="+20%" rate="110%" pitch="+15%">$TEXT</prosody>',
            description: 'For key points'
        },
        gentle: {
            pattern: '<prosody volume="-10%" rate="90%" pitch="-10%">$TEXT</prosody>',
            description: 'For calming moments'
        },
        dramatic: {
            pattern: '<prosody pitch="-15%" rate="80%">$TEXT</prosody>',
            description: 'For serious moments'
        }
    },
    breaks: {
        extra_short: {
            pattern: '<break time="250ms"/>',
            description: 'Very slight pause for quick rhythm changes'
        },
        short: {
            pattern: '<break time="500ms"/>',
            description: 'Brief pause'
        },
        medium: {
            pattern: '<break time="1s"/>',
            description: 'Standard pause'
        },
        long: {
            pattern: '<break time="2s"/>',
            description: 'Dramatic pause'
        },
        extra_long: {
            pattern: '<break time="3s"/>',
            description: 'Extended pause for high-impact moments'
        },
        thought_pause: {
            pattern: '<break time="400ms"/><prosody rate="95%">$TEXT</prosody>',
            description: 'For contemplative transitions'
        },
        dramatic_pause: {
            pattern: '<break time="2s"/><prosody pitch="-10%">$TEXT</prosody>',
            description: 'For impact moments'
        }
    },
    effects: {
        drc: {
            pattern: '<amazon:effect name="drc"><prosody volume="+10%">$TEXT</prosody></amazon:effect>',
            description: 'Enhanced clarity with emphasis'
        },
        pronunciation: {
            pattern: '<sub alias="$ALIAS"><prosody rate="98%">$TEXT</prosody></sub>',
            description: 'Clear pronunciation'
        },
        urgent_whisper: {
            pattern: '<amazon:effect name="whispered"><prosody rate="fast" pitch="+10%">$TEXT</prosody></amazon:effect>',
            description: 'For urgent secrets'
        },
        clear_emphasis: {
            pattern: '<amazon:effect name="drc"><prosody volume="+20%">$TEXT</prosody></amazon:effect>',
            description: 'For clear, emphasized points'
        }
    },
    character: {
        ursula_stern: {
            pattern: '<prosody pitch="-10%" rate="90%"><amazon:emotion name="disappointed" intensity="medium">$TEXT</amazon:emotion></prosody>',
            description: 'For stern moments'
        },
        ursula_proud: {
            pattern: '<amazon:emotion name="happy" intensity="high"><prosody pitch="+15%">$TEXT</prosody></amazon:emotion>',
            description: 'For proud moments'
        },
        ursula_excited: {
            pattern: '<amazon:emotion name="excited" intensity="high"><prosody rate="+15%" pitch="+20%">$TEXT</prosody></amazon:emotion>',
            description: 'For enthusiastic moments'
        },
        ursula_caring: {
            pattern: '<amazon:emotion name="happy" intensity="low"><prosody volume="soft" rate="95%">$TEXT</prosody></amazon:emotion>',
            description: 'For nurturing moments'
        }
    },
    transitions: {
        topic_change: {
            pattern: '<break time="1s"/><prosody pitch="+10%" rate="110%">$TEXT</prosody>',
            description: 'For switching topics'
        },
        build_up: {
            pattern: '<prosody rate="85%">$TEXT</prosody><break time="300ms"/><prosody rate="110%" pitch="+15%">$TEXT</prosody>',
            description: 'For building tension'
        },
        wind_down: {
            pattern: '<prosody rate="110%" pitch="+10%">$TEXT</prosody><break time="500ms"/><prosody rate="90%" pitch="-5%">$TEXT</prosody>',
            description: 'For concluding thoughts'
        }
    }
};

module.exports = ssmlPatterns; 