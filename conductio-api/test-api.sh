#!/bin/bash

# Test script for Conductio API

API_BASE="http://localhost:3001/api"

echo "🧪 Testing Conductio API..."
echo "=========================="

# Test 1: Health Check
echo "📋 Test 1: Health Check"
curl -s -w "\nStatus: %{http_code}\n" "$API_BASE/health" | head -10
echo

# Test 2: API Info
echo "📋 Test 2: API Documentation"
curl -s -w "\nStatus: %{http_code}\n" "$API_BASE/health/info" | head -10
echo

# Test 3: List Instruments
echo "📋 Test 3: List Instruments"
curl -s -w "\nStatus: %{http_code}\n" "$API_BASE/instruments" | head -10
echo

# Test 4: Generate and Stream MIDI (Quick Test)
echo "📋 Test 4: Generate and Stream MIDI"
curl -X POST "$API_BASE/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "layer": "melody",
    "key": "C major",
    "bpm": 120,
    "bars": 4,
    "instrument": "acoustic_grand_piano",
    "genre": "jazz",
    "renderAudio": false
  }' \
  -w "\nHTTP Status: %{http_code}\nContent-Type: %{content_type}\n" \
  -o "test-melody.mid"

if [ -f "test-melody.mid" ]; then
  echo "✅ MIDI file downloaded: $(ls -lh test-melody.mid)"
else
  echo "❌ MIDI file not downloaded"
fi

echo

# Test 5: Generate and Stream Audio (if available)
echo "📋 Test 5: Generate and Stream Audio"
curl -X POST "$API_BASE/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "layer": "melody",
    "key": "F major",
    "bpm": 100,
    "bars": 2,
    "instrument": "electric_piano_1",
    "genre": "blues",
    "renderAudio": true
  }' \
  -w "\nHTTP Status: %{http_code}\nContent-Type: %{content_type}\n" \
  -o "test-blues.wav"

if [ -f "test-blues.wav" ]; then
  echo "✅ Audio file downloaded: $(ls -lh test-blues.wav)"
else
  echo "❌ Audio file not downloaded"
fi

echo

# Test 6: Async Generation (for comparison)
echo "📋 Test 6: Async Generation"
JOB_RESPONSE=$(curl -s -X POST "$API_BASE/generate/async" \
  -H "Content-Type: application/json" \
  -d '{
    "layer": "bass",
    "key": "E minor",
    "bpm": 140,
    "bars": 8,
    "genre": "rock"
  }')

echo "Async Response:"
echo "$JOB_RESPONSE"

echo
echo "✅ API Testing Complete!"