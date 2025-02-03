const { handleUrsulaRequest } = require('./ursula_api_node');

async function runTests() {
    // Test cases
    const tests = [
        {
            name: 'Get Relationship',
            input: {
                item: {
                    json: {
                        endpoint: '/memory/relationships/russ',
                        method: 'GET'
                    }
                }
            }
        },
        {
            name: 'Get Medical Stories',
            input: {
                item: {
                    json: {
                        endpoint: '/memory/stories/medical',
                        method: 'GET'
                    }
                }
            }
        },
        {
            name: 'Store Memory',
            input: {
                item: {
                    json: {
                        endpoint: '/memory/store',
                        method: 'POST',
                        body: {
                            category: 'medical',
                            content: {
                                task: 'Return screening kit',
                                status: 'pending',
                                due_date: '2024-03-01'
                            },
                            context: 'urgent'
                        }
                    }
                }
            }
        },
        {
            name: 'Get Voicemail Template',
            input: {
                item: {
                    json: {
                        endpoint: '/voicemail/templates/medical_urgent',
                        method: 'GET'
                    }
                }
            }
        }
    ];

    // Run tests
    for (const test of tests) {
        console.log(`\nRunning test: ${test.name}`);
        try {
            const result = await handleUrsulaRequest(test.input);
            console.log('Success:', JSON.stringify(result, null, 2));
        } catch (error) {
            console.error('Error:', error.message);
        }
    }
}

// Run tests if called directly
if (require.main === module) {
    runTests().catch(console.error);
} 