#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Base URL
BASE_URL="http://192.168.0.63:8080"

# Function to test endpoint
test_endpoint() {
    local endpoint=$1
    local method=${2:-GET}
    local data=${3:-""}
    
    echo -n "Testing $method $endpoint... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "%{http_code}" "$BASE_URL$endpoint")
    else
        response=$(curl -s -w "%{http_code}" -X "$method" -H "Content-Type: application/json" -d "$data" "$BASE_URL$endpoint")
    fi
    
    http_code=${response: -3}
    response_body=${response:0:${#response}-3}
    
    if [[ $http_code -ge 200 && $http_code -lt 300 ]]; then
        echo -e "${GREEN}OK${NC} ($http_code)"
        echo "$response_body" | jq '.' 2>/dev/null || echo "$response_body"
    else
        echo -e "${RED}FAILED${NC} ($http_code)"
        echo "$response_body"
    fi
    echo "----------------------------------------"
}

echo "Starting API endpoint tests..."
echo "=========================================="

# Health Check
test_endpoint "/health"

# Universe APIs
test_endpoint "/universe/family"
test_endpoint "/universe/characters"
test_endpoint "/universe/locations"
test_endpoint "/universe/rules"
test_endpoint "/universe/relationships"
test_endpoint "/universe/network"

# Task Management APIs
test_endpoint "/tasks/RED" # Test each priority
test_endpoint "/tasks/ORANGE"
test_endpoint "/tasks/YELLOW"
test_endpoint "/tasks/GREEN"
test_endpoint "/tasks/escalations/medical"
test_endpoint "/tasks"
test_endpoint "/tasks/subtasks/1"
test_endpoint "/tasks/1/complete" "PUT"
test_endpoint "/tasks/1/notes" "PUT" '{"notes": "Test note"}'
test_endpoint "/tasks/process" "POST"
test_endpoint "/tasks/rollcall"

# Voice Pattern APIs
test_endpoint "/voice/patterns/emotions"
test_endpoint "/voice/patterns/prosody"
test_endpoint "/voice/patterns/breaks"
test_endpoint "/voice/patterns/character"

# Russ Management APIs
test_endpoint "/russ/profiles"
test_endpoint "/russ/patterns"
test_endpoint "/russ/triggers"
test_endpoint "/russ/escalation/1"
test_endpoint "/russ/stories"
test_endpoint "/russ/family"

# Task AI Enrichment
test_endpoint "/tasks/ai_enrich" "POST" '{"task_id": "1"}'
test_endpoint "/tasks/ai_rollcall" "POST"

# Task Import
test_endpoint "/tasks/todoist/import/full" "POST"
test_endpoint "/tasks/todoist/sync"

# Data Ingestion
test_endpoint "/ingest/raw" "POST" '{"source": "email", "content": {}, "metadata": {}}'
test_endpoint "/ingest/status/1"
test_endpoint "/ingest/pending"

# Webhook
test_endpoint "/webhook/todoist" "POST" '{"event_type": "task_update", "data": {}}'
test_endpoint "/webhook/config/todoist"

echo "=========================================="
echo "API endpoint tests completed"
