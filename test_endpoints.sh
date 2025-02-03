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
    
    # URL encode the endpoint
    encoded_endpoint=$(echo "$endpoint" | sed 's/ /%20/g')
    
    echo -e "\nTesting ${method} ${endpoint}"
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "${BASE_URL}${encoded_endpoint}")
    else
        response=$(curl -s -w "\n%{http_code}" -X ${method} "${BASE_URL}${encoded_endpoint}" -H "Content-Type: application/json" -d "${data}")
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

# Test Relationships
echo -e "\n=== Testing Relationships ==="
test_endpoint "/api/ursula/memory/relationships/Russ"
test_endpoint "/api/ursula/memory/relationships/Charlotte"
test_endpoint "/api/ursula/memory/relationships/Big%20Mickie"

# Test Stories
echo -e "\n=== Testing Stories ==="
test_endpoint "/api/ursula/memory/stories/medical_warning"
test_endpoint "/api/ursula/memory/stories/responsibility"

# Test Patterns
echo -e "\n=== Testing Patterns ==="
test_endpoint "/api/ursula/patterns/emotion"
test_endpoint "/api/ursula/patterns/prosody"
test_endpoint "/api/ursula/patterns/break"
test_endpoint "/api/ursula/patterns/character"
test_endpoint "/api/ursula/patterns/effect"

# Test Templates
echo -e "\n=== Testing Templates ==="
test_endpoint "/api/ursula/voicemail/templates/medical_urgent"
test_endpoint "/api/ursula/voicemail/templates/general_update"

# Test SSML Build
echo -e "\n=== Testing SSML Build ==="
test_endpoint "/api/ursula/ssml/build" "POST" '{"text": "Hello", "pattern_type": "emotion", "pattern_name": "caring"}'
