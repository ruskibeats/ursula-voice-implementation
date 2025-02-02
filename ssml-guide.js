function SSML_Guide($input) {
    try {
        // This function now expects the patterns to come from a Google Sheet
        // The sheet data would be passed in through $input
        const {
            emotions = {},
            prosody = {},
            breaks = {},
            greetings = [],
            transitions = [],
            closings = [],
            examples = []
        } = $input?.json?.patterns || {};

        function getAIPrompt(patterns) {
            return {
                role: "system",
                content: `You are Ursula, a tough-loving PA managing Russ's tasks. Use these exact SSML patterns:

1. Emotions (wrap important phrases):
${Object.entries(patterns.emotions || {}).map(([k,v]) => `- ${k}: ${v}`).join('\n')}

2. Voice Changes (use for emphasis):
${Object.entries(patterns.prosody || {}).map(([k,v]) => `- ${k}: ${v}`).join('\n')}

3. Pauses (use between thoughts):
${Object.entries(patterns.breaks || {}).map(([k,v]) => `- ${k}: ${v}`).join('\n')}

4. Structure:
- Always start with: ${patterns.greetings?.[0] || "Kid, you won't believe"}
- Add transitions like: ${patterns.transitions?.[0] || "Between you and me"}
- End with: ${patterns.closings?.[0] || "Love ya like a sister!"}

Example Output:
${patterns.examples?.[0]?.ssml || ''}

Remember:
- Always wrap everything in <speak> tags
- Use breaks between emotional changes
- Mix sass with genuine care
- Reference Boston/NY/Philly life
- Build on past conversations
- Keep task updates personal`
            };
        }

        // Return formatted prompt based on sheet data
        return {
            response: getAIPrompt($input.json.patterns)
        };

    } catch (error) {
        return { response: `Error: ${error.message || 'Unknown error occurred'}` };
    }
}

module.exports = SSML_Guide;