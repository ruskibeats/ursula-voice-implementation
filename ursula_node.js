const { NodeOperationError } = require('n8n-workflow');

class UrsulaNode {
    constructor() {
        this.id = 'ursulaApi';
        this.name = 'Ursula API';
        this.icon = '🗣️';
        this.group = ['ai'];
        this.version = 1;
        this.description = 'Access Ursula\'s memory and voice patterns';
        this.defaults = {
            name: 'Ursula API',
        };
        this.inputs = ['main'];
        this.outputs = ['main'];
    }

    async execute(this.getNode()) {
        const items = this.getInputData();
        const returnData = [];
        const baseUrl = 'http://192.168.0.63:8080/api/ursula';

        for (let i = 0; i < items.length; i++) {
            try {
                const endpoint = this.getNodeParameter('endpoint', i);
                const method = this.getNodeParameter('method', i);
                
                // Build URL with query parameters for GET requests
                let url = `${baseUrl}${endpoint}`;
                if (method === 'GET') {
                    const parameters = this.getNodeParameter('parameters', i, {});
                    if (parameters.parameter) {
                        const queryParams = parameters.parameter
                            .map(param => `${encodeURIComponent(param.key)}=${encodeURIComponent(param.value)}`)
                            .join('&');
                        if (queryParams) {
                            url += `?${queryParams}`;
                        }
                    }
                }

                // Build request options
                const options = {
                    method,
                    headers: {
                        'Content-Type': 'application/json',
                    },
                };

                // Add body for POST requests
                if (method === 'POST') {
                    const body = this.getNodeParameter('body', i);
                    options.body = JSON.stringify(body);
                }

                // Make request
                const response = await fetch(url, options);
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                
                returnData.push({
                    json: data
                });
            } catch (error) {
                if (this.continueOnFail()) {
                    returnData.push({
                        json: {
                            error: error.message
                        },
                        error: error.message,
                    });
                    continue;
                }
                throw new NodeOperationError(this.getNode(), error);
            }
        }
        
        return [returnData];
    }
}

module.exports = { nodeClass: UrsulaNode }; 