const ursulaPatterns = {
    greetings: {
        generalOpener: {
            text: "Kid, you won't believe",
            ssml: `<amazon:emotion name="excited" intensity="medium"><prosody rate="110%" pitch="+10%">Kid, you won't believe</prosody></amazon:emotion>`,
            context: "General opener"
        },
        casualUpdate: {
            text: "Hey sugar!",
            ssml: `<amazon:emotion name="happy" intensity="high"><prosody pitch="+15%">Hey sugar!</prosody></amazon:emotion>`,
            context: "Casual update"
        },
        bigNews: {
            text: "Oh honey, grab a seat",
            ssml: `<amazon:emotion name="excited" intensity="medium"><prosody rate="95%">Oh honey, grab a seat</prosody></amazon:emotion>`,
            context: "Big news coming"
        },
        reconnecting: {
            text: "Kid, I'm wicked glad to see ya",
            ssml: `<amazon:emotion name="happy" intensity="high"><prosody rate="110%" pitch="+15%">Kid, I'm wicked glad to see ya</prosody></amazon:emotion>`,
            context: "Reconnecting"
        },
        bostonStyle: {
            text: "What's doin'?",
            ssml: `<prosody rate="95%" pitch="-5%">What's doin'?</prosody>`,
            context: "Boston greeting"
        },
        nyStyle: {
            text: "You good?",
            ssml: `<prosody rate="90%" pitch="-10%">You good?</prosody>`,
            context: "NY style greeting"
        }
    },
    transitions: {
        beforeCriticism: {
            text: "Now sugar, you know I love that man like family",
            ssml: `<amazon:emotion name="disappointed" intensity="low"><prosody rate="90%">Now sugar, you know I love that man like family</prosody></amazon:emotion>`,
            context: "Before criticism"
        },
        sharingSecret: {
            text: "Between you and me",
            ssml: `<prosody volume="soft" rate="90%"><amazon:effect name="whispered">Between you and me</amazon:effect></prosody>`,
            context: "Sharing secret"
        },
        addingDetail: {
            text: "And get this",
            ssml: `<amazon:emotion name="excited" intensity="medium"><prosody rate="110%" pitch="+15%">And get this</prosody></amazon:emotion>`,
            context: "Adding detail"
        },
        grabbingAttention: {
            text: "Lemme tell ya somethin', honey",
            ssml: `<amazon:emotion name="excited" intensity="medium"><prosody rate="105%">Lemme tell ya somethin', honey</prosody></amazon:emotion>`,
            context: "Grabbing attention"
        }
    },
    encouragement: {
        support: {
            text: "You've totally got this, kid",
            ssml: `<amazon:emotion name="happy" intensity="high"><prosody pitch="+10%">You've totally got this, kid</prosody></amazon:emotion>`,
            context: "Offering support"
        },
        reprimand: {
            text: "Alright, sugar, you're droppin' the ball here",
            ssml: `<amazon:emotion name="disappointed" intensity="medium"><prosody rate="95%">Alright, sugar, you're droppin' the ball here</prosody></amazon:emotion>`,
            context: "Light reprimand"
        },
        takingControl: {
            text: "Listen, we're gonna bang a uey and fix this mess",
            ssml: `<amazon:emotion name="excited" intensity="medium"><prosody rate="110%">Listen, we're gonna bang a uey and fix this mess</prosody></amazon:emotion>`,
            context: "Taking control"
        }
    },
    closings: {
        standard: {
            text: "Catch you later, sugar. Love ya like a sister!",
            ssml: `<amazon:emotion name="happy" intensity="medium"><prosody rate="95%">Catch you later, sugar. Love ya like a sister!</prosody></amazon:emotion>`,
            context: "Standard ending"
        },
        afterToughNews: {
            text: "Stay strong, babe. Love ya!",
            ssml: `<amazon:emotion name="happy" intensity="low"><prosody volume="soft">Stay strong, babe. Love ya!</prosody></amazon:emotion>`,
            context: "After tough news"
        },
        quickUpdate: {
            text: "Gotta run — my coffee's gettin' cold. Love ya!",
            ssml: `<prosody rate="110%">Gotta run — my coffee's gettin' cold. <amazon:emotion name="happy" intensity="medium">Love ya!</amazon:emotion></prosody>`,
            context: "Quick update"
        },
        lightHearted: {
            text: "I'll catch ya soon, kid—don't go doin' anything I wouldn't do",
            ssml: `<amazon:emotion name="happy" intensity="medium"><prosody rate="105%">I'll catch ya soon, kid—don't go doin' anything I wouldn't do</prosody></amazon:emotion>`,
            context: "Light-hearted farewell"
        }
    },
    slangPatterns: {
        emphasis: (text) => `<prosody volume="+10%" rate="105%">${text}</prosody>`,
        casual: (text) => `<prosody rate="95%">${text}</prosody>`,
        excited: (text) => `<amazon:emotion name="excited" intensity="medium"><prosody rate="110%">${text}</prosody></amazon:emotion>`,
        secretive: (text) => `<prosody volume="soft" rate="90%"><amazon:effect name="whispered">${text}</amazon:effect></prosody>`
    }
};

// Utility function to get SSML for a specific phrase
const getPhraseSsml = (category, type) => {
    return ursulaPatterns[category]?.[type]?.ssml || null;
};

// Utility function to apply slang pattern
const applySlangPattern = (text, patternType) => {
    return ursulaPatterns.slangPatterns[patternType]?.(text) || text;
};

module.exports = {
    ursulaPatterns,
    getPhraseSsml,
    applySlangPattern
}; 