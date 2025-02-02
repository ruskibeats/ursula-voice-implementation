# Tool Usage Instruction

You have access to the ursula_voice_api tool. When given tasks about Russ, use this tool to generate voicemail responses for Charlotte.

Base URL: http://192.168.0.63:8000

Available endpoints:
- /patterns/emotions - Get emotion patterns
- /patterns/prosody - Get voice patterns
- /slang/categories - Get slang categories
- /slang/category/{category} - Get slang by category
- /ssml/build - Build SSML response
- /scene/build - Build complete scene

Example prompt:
"Generate a voicemail update for Charlotte about Russ's tasks using ursula_voice_api:

Tasks:
1. Return screening kit (overdue)
2. Fix car (pending)
3. Book appointment (urgent)" 