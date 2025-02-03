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
    local data=$3
    
    echo -e "\nTesting ${method} ${endpoint}"
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "${BASE_URL}${endpoint}")
    else
        response=$(curl -s -w "\n%{http_code}" -X ${method} "${BASE_URL}${endpoint}" -H "Content-Type: application/json" -d "${data}")
    fi
    
    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$status_code" -eq 200 ]; then
        echo -e "${GREEN}✓ Success${NC} (${status_code})"
        echo "Response: $body"
    else
        echo -e "${RED}✗ Failed${NC} (${status_code})"
        echo "Response: $body"
    fi
}

# Memory Endpoints
test_endpoint "/api/ursula/memory/relationships/russ"
test_endpoint "/api/ursula/memory/stories/medical"
test_endpoint "/api/ursula/memory/recent/medical"

# Pattern Endpoints
test_endpoint "/api/ursula/patterns/emotion"
test_endpoint "/api/ursula/patterns/successful/greeting"
test_endpoint "/api/ursula/stats/patterns"

# Character Endpoints
test_endpoint "/api/ursula/character/traits"
test_endpoint "/api/ursula/character/traits/voice"

# Story Endpoints
test_endpoint "/api/ursula/stories/favorite"

# Template Endpoints
test_endpoint "/api/ursula/templates/greeting"
test_endpoint "/api/ursula/voicemail/templates"

# SSML Endpoints
test_endpoint "/api/ursula/ssml/build" "POST" '{"text": "Hello", "pattern_type": "greeting", "pattern_name": "casual"}'
test_endpoint "/api/ursula/slang/build" "POST" '{"term": "wicked"}'

# Interaction History
test_endpoint "/api/ursula/memory/interactions/russ"

