# Ursula Voice API Tool

{
    "name": "ursula_voice_api",
    "description": "FastAPI service that generates SSML-formatted voice responses with Boston-style personality. Provides patterns for emotions, voice modulation, and regional slang. Takes task lists and returns voicemail-style updates in Ursula's voice.",
    "base_url": "http://192.168.0.63:8000",
    "parameters": {
        "type": "object",
        "properties": {
            "endpoint": {
                "type": "string",
                "enum": [
                    "/patterns/emotions",
                    "/patterns/prosody",
                    "/slang/categories",
                    "/slang/category/{category}",
                    "/ssml/build",
                    "/scene/build"
                ]
            },
            "task_list": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": "string",
                        "status": "string",
                        "due_date": "string"
                    }
                }
            }
        },
        "required": ["endpoint"]
    },
    "returns": {
        "type": "object",
        "properties": {
            "ssml": "string",
            "patterns": "array",
            "slang": "array"
        }
    },
    "examples": [
        {
            "input": {
                "endpoint": "/scene/build",
                "task_list": [{"name": "Return screening kit", "status": "pending"}]
            },
            "output": {
                "ssml": "<speak><amazon:emotion>...</amazon:emotion></speak>"
            }
        }
    ]
} 