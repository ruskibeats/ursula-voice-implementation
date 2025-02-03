const BASE_URL = 'http://192.168.0.63:8080/api/ursula';

async function handleUrsulaRequest($input) {
    const { endpoint, method = 'GET', params = {}, body = null } = $input.item.json;

    // Build URL with query parameters
    const queryString = Object.keys(params)
        .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
        .join('&');
    const url = `${BASE_URL}${endpoint}${queryString ? `?${queryString}` : ''}`;

    // Build request options
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };

    // Add body for POST/PUT requests
    if (body && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return { json: data };
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Example usage in n8n:
// Input format:
// {
//     "endpoint": "/memory/relationships/russ",
//     "method": "GET"
// }
// or
// {
//     "endpoint": "/memory/store",
//     "method": "POST",
//     "body": {
//         "category": "medical",
//         "content": {...},
//         "context": "urgent"
//     }
// }

module.exports = {
    handleUrsulaRequest
}; 