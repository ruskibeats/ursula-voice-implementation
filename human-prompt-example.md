# Example Human Prompts for Ursula

"Hey Ursula, here's Russ's task list for today - can you give Charlotte an update?

Tasks:
1. Return bowel cancer screening kit (due last week)
2. Fix the beetle on driveway (been there 3 days)
3. Sort out Land Rover service booking (needs doing ASAP)

Use the voice API at http://192.168.0.63:8000 to build your response."

# Alternative Format:

"Ursula, Charlotte needs your daily Russ report. Here's what he's supposed to be doing:
{
    'tasks': [
        {
            'name': 'Return screening kit',
            'status': 'pending',
            'due_date': '2024-03-01'
        },
        {
            'name': 'Fix beetle on driveway',
            'status': 'pending',
            'due_date': '2024-03-10'
        }
    ]
}

Give her your usual voicemail update using the voice API." 