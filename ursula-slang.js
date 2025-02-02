const { applySlangPattern } = require('./ursula-phrases');

const slangTerms = {
    // Boston-specific terms
    wicked: {
        term: "wicked",
        meaning: "Very",
        example: "That's wicked cool.",
        pattern: "emphasis"
    },
    packie: {
        term: "packie",
        meaning: "Liquor store",
        example: "Heading to the packie.",
        pattern: "casual"
    },
    bubbler: {
        term: "bubbler",
        meaning: "Drinking fountain",
        example: "Get some water at the bubbler.",
        pattern: "casual"
    },
    
    // Common slang
    masshole: {
        term: "Masshole",
        meaning: "Massachusetts resident (prideful)",
        example: "Proud to be a Masshole.",
        pattern: "excited"
    },
    frappe: {
        term: "frappe",
        meaning: "Milkshake",
        example: "Get me a chocolate frappe.",
        pattern: "casual"
    },
    
    // Directional terms
    bangAUey: {
        term: "bang a U-ey",
        meaning: "Make a U-turn",
        example: "Bang a U-ey at the light.",
        pattern: "emphasis"
    },
    upTheCorner: {
        term: "up the corner",
        meaning: "Neighborhood hangout",
        example: "He's up the corner with his boys.",
        pattern: "casual"
    },
    
    // Food related
    grinder: {
        term: "grinder",
        meaning: "Sub sandwich",
        example: "Grab me a grinder.",
        pattern: "casual"
    },
    tonic: {
        term: "tonic",
        meaning: "Soda",
        example: "Get me a tonic.",
        pattern: "casual"
    },
    
    // Social terms
    kid: {
        term: "kid",
        meaning: "Friend/person",
        example: "Listen, kid.",
        pattern: "emphasis"
    },
    sugar: {
        term: "sugar",
        meaning: "Term of endearment",
        example: "Hey sugar!",
        pattern: "emphasis"
    }
};

// Get SSML for a slang term
const getSlangSsml = (term) => {
    const slangInfo = slangTerms[term];
    if (!slangInfo) return null;
    return applySlangPattern(slangInfo.term, slangInfo.pattern);
};

// Get example with SSML
const getSlangExample = (term) => {
    const slangInfo = slangTerms[term];
    if (!slangInfo) return null;
    
    const ssmlTerm = applySlangPattern(slangInfo.term, slangInfo.pattern);
    return slangInfo.example.replace(slangInfo.term, ssmlTerm);
};

// Get all terms of a specific pattern type
const getTermsByPattern = (patternType) => {
    return Object.values(slangTerms)
        .filter(term => term.pattern === patternType)
        .map(term => term.term);
};

module.exports = {
    slangTerms,
    getSlangSsml,
    getSlangExample,
    getTermsByPattern
}; 