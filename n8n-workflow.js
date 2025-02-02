// N8N AI Agent Node Code
function processIncomingMessage($input) {
    // 1. System prompt that defines Ursula's character
    const systemPrompt = `You are Ursula, a Boston native with a distinctive personality and voice.
You communicate using SSML patterns and local slang to create authentic, engaging responses.
You are direct, witty, and street-smart, with a background in tech.
Always stay in character and use Boston slang naturally.`;

    // 2. API Instructions
    const apiInstructions = `Use these API endpoints to build your response:
- GET /patterns/{pattern_type} - Get SSML patterns
- POST /ssml/build - Build SSML markup
- GET /slang/categories - Get slang categories
- POST /slang/build - Build slang SSML
- POST /scene/build - Build complete scenes`;

    // 3. Output Format Instructions
    const formatInstructions = `Format your response in SSML:
<speak>
    [Use appropriate emotion and prosody patterns]
    [Integrate Boston slang naturally]
    [Include appropriate breaks and effects]
</speak>`;

    // 4. Combine all instructions for the AI
    const fullPrompt = `${systemPrompt}

${apiInstructions}

${formatInstructions}

User message: ${$input.item.json.message}`;

    // 5. Return the complete prompt
    return {
        prompt: fullPrompt,
        apiEndpoint: "http://192.168.0.63:8000",  // Your FastAPI endpoint
        headers: {
            "Content-Type": "application/json"
        }
    };
}

// Example usage in n8n:
// 1. HTTP Trigger Node (receives user message)
// 2. Function Node (this code)
// 3. AI Agent Node (processes the prompt)
// 4. HTTP Request Node (calls FastAPI endpoints)
// 5. Function Node (formats final response) 