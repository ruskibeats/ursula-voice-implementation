#!/bin/bash

# Database connection details
HOST="192.168.0.169"
USER="russbee"
DB="beehive"
PASSWORD="skimmer69"
OUTPUT_FILE="output_data.txt"

# Export data to a file
export PGPASSWORD=$PASSWORD

# Run SQL commands and output to a file
psql -h $HOST -U $USER -d $DB -o $OUTPUT_FILE <<EOF
SELECT * FROM character_profiles;
SELECT * FROM family;  
SELECT * FROM escalation_triggers;  
SELECT * FROM relationships;  
SELECT * FROM character_profiles;  
SELECT * FROM data_sources;  
SELECT * FROM processing_rules;  
SELECT * FROM peak_performance_tracking;  
SELECT * FROM priority_matrix;  
SELECT * FROM red_flags;  
SELECT * FROM ai_commands;  
SELECT * FROM task_patterns;  
SELECT * FROM response_triggers;  
SELECT * FROM tasks_subtasks;  
SELECT * FROM escalation_system;  
SELECT * FROM loyalty_stories;  
SELECT * FROM charlotte_perspective;  
SELECT * FROM daily_routines;  
SELECT * FROM personal_rules;  
SELECT * FROM regional_traits;  
SELECT * FROM secret_skills;  
SELECT * FROM vulnerabilities;  
SELECT * FROM regular_haunts;  
SELECT * FROM future_dreams;  
SELECT * FROM guilty_pleasures;  
SELECT * FROM family_members;  
SELECT * FROM task_roll_call;  
SELECT * FROM task_grading_factors;  
SELECT * FROM task_analytics;  
SELECT * FROM data_ingest_queue;  
SELECT * FROM daily_roll_call;  
SELECT * FROM task_priority;  
SELECT * FROM recurring_tasks;  
SELECT * FROM background_stories;  
SELECT * FROM character_backstories;  
SELECT * FROM story_locations;  
SELECT * FROM life_philosophies;  
SELECT * FROM character_traits;  
SELECT * FROM trust_system;
EOF

# Unset the password variable for security
unset PGPASSWORD

echo "Data export completed. Check the file: $OUTPUT_FILE"
