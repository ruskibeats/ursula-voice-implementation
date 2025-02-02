const { ursulaPatterns, getPhraseSsml } = require('./ursula-phrases');
const { getSlangSsml, getSlangExample, slangTerms } = require('./ursula-slang');

// Example 1: Basic greeting
function demonstrateGreeting() {
    // Get a standard greeting
    const greeting = getPhraseSsml('greetings', 'generalOpener');
    return `<speak>${greeting}</speak>`;
}

// Example 2: Complete conversation
function buildConversation(topic = "gossip") {
    const conversation = [];
    
    // Opening
    conversation.push(getPhraseSsml('greetings', 'bigNews'));
    
    // Transition to topic
    conversation.push(getPhraseSsml('transitions', 'sharingSecret'));
    
    // Add some slang
    const slangExample = getSlangExample('wicked');
    conversation.push(slangExample);
    
    // Closing
    conversation.push(getPhraseSsml('closings', 'standard'));
    
    return `<speak>${conversation.join(' ')}</speak>`;
}

// Example 3: Dynamic phrase building
function buildCustomPhrase(text, emotion = "happy", intensity = "medium") {
    return `<speak>
        <amazon:emotion name="${emotion}" intensity="${intensity}">
            ${text}
        </amazon:emotion>
    </speak>`;
}

// Example 4: Using slang in context
function useSlangsInSentence() {
    const sentence = "Let's bang a U-ey at the packie and grab some tonic.";
    
    // Replace slang terms with SSML versions
    let ssmlSentence = sentence;
    ['bangAUey', 'packie', 'tonic'].forEach(term => {
        const slangSsml = getSlangSsml(term);
        if (slangSsml) {
            ssmlSentence = ssmlSentence.replace(slangTerms[term].term, slangSsml);
        }
    });
    
    return `<speak>${ssmlSentence}</speak>`;
}

// Example 5: Building a complete scene
function buildScene(mood = "excited") {
    const scene = [];
    
    // Opening with mood-appropriate greeting
    if (mood === "excited") {
        scene.push(getPhraseSsml('greetings', 'generalOpener'));
    } else {
        scene.push(getPhraseSsml('greetings', 'casualUpdate'));
    }
    
    // Add transition
    scene.push(getPhraseSsml('transitions', 'addingDetail'));
    
    // Add some Boston slang
    scene.push(getSlangExample('wicked'));
    scene.push(getSlangExample('masshole'));
    
    // Close appropriately
    if (mood === "excited") {
        scene.push(getPhraseSsml('closings', 'lightHearted'));
    } else {
        scene.push(getPhraseSsml('closings', 'standard'));
    }
    
    return `<speak>${scene.join(' ')}</speak>`;
}

// Usage examples
console.log("Basic Greeting:");
console.log(demonstrateGreeting());

console.log("\nComplete Conversation:");
console.log(buildConversation());

console.log("\nCustom Phrase:");
console.log(buildCustomPhrase("Sugar, you ain't gonna believe this tea!", "excited", "high"));

console.log("\nSlang in Context:");
console.log(useSlangsInSentence());

console.log("\nComplete Scene (Excited):");
console.log(buildScene("excited")); 