# Conductio API Documentation

Complete API reference for the Conductio AI Music Generation System.

## Table of Contents

- [Authentication](#authentication)
- [Base URL](#base-url)
- [Request Format](#request-format)
- [Response Format](#response-format)
- [Endpoints](#endpoints)
- [Generation Parameters](#generation-parameters)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

## Authentication

Currently, no authentication is required. The API is open for development and testing.

## Base URL

```
http://localhost:3001/api
```

## Request Format

All requests must be sent as JSON with the `Content-Type: application/json` header.

## Response Format

All responses follow this standard format:

```json
{
  "success": boolean,
  "data": object | null,
  "error": string | null,
  "message": string | null
}
```

---

## Endpoints

### Health & Information

#### `GET /health`
Check API health and engine availability.

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2025-11-07T13:45:00.000Z",
    "uptime": 3600,
    "version": "1.0.0",
    "services": {
      "conductioEngine": "available",
      "python": "available"
    }
  }
}
```

#### `GET /health/info`
Get API documentation and examples.

---

### Music Generation

#### `POST /generate` - **Stream Generation** ⭐
Generate music and stream the file directly back to the client.

**Request Body:**
```json
{
  "layer": "melody",           // Required: "melody" | "bass" | "drums" | "chords"
  "key": "C major",            // Optional: Any musical key (default: "C minor")
  "bpm": 120,                  // Optional: 60-200 (default: 120)
  "bars": 8,                   // Optional: 1-64 (default: 8)
  "instrument": "acoustic_grand_piano", // Optional: GM instrument (default: "auto")
  "genre": "jazz",             // Optional: Any genre (default: "general")
  "renderAudio": true          // Optional: true/false (default: true)
}
```

**Response:**
- **Success**: Streams the generated file directly (WAV or MIDI)
- **Headers**: 
  - `Content-Type`: `audio/wav` or `audio/midi`
  - `Content-Disposition`: `attachment; filename="creative_name_layer.ext"`
  - `X-Generation-Info`: JSON with generation details

#### `POST /generate/async` - **Async Generation**
Start generation and return job ID for later retrieval.

**Request Body:** Same as `/generate`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid-job-id",
    "layer": "melody",
    "genre": "jazz",
    "key": "C major",
    "bpm": 120,
    "bars": 8,
    "instrument": "acoustic_grand_piano",
    "outputPath": "",
    "midiFile": "",
    "createdAt": "2025-11-07T13:45:00.000Z"
  }
}
```

#### `GET /generate/status/:id`
Check the status of an async generation job.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid-job-id",
    "status": "completed", // "pending" | "processing" | "completed" | "failed"
    "request": { /* original request */ },
    "result": { /* generation result */ },
    "error": null,
    "createdAt": "2025-11-07T13:45:00.000Z"
  }
}
```

#### `GET /generate/download/:id/:type`
Download files from completed async generation.

**Parameters:**
- `id`: Job ID from async generation
- `type`: `midi` or `audio`

**Response:** File stream

---

### Instruments

#### `GET /instruments`
List all available instruments.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 0,
      "name": "acoustic_grand_piano",
      "displayName": "Acoustic Grand Piano",
      "category": "Piano"
    },
    // ... 127 more instruments
  ]
}
```

#### `GET /instruments/categories`
List instruments organized by category.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "name": "Piano",
      "instruments": [
        {
          "id": 0,
          "name": "acoustic_grand_piano",
          "displayName": "Acoustic Grand Piano",
          "category": "Piano"
        }
        // ... more piano instruments
      ]
    }
    // ... more categories
  ]
}
```

---

## Generation Parameters

### Required Parameters

| Parameter | Type | Description | Values |
|-----------|------|-------------|---------|
| `layer` | string | Type of musical layer to generate | `"melody"` \| `"bass"` \| `"drums"` \| `"chords"` |

### Optional Parameters

| Parameter | Type | Default | Description | Valid Values |
|-----------|------|---------|-------------|--------------|
| `key` | string | `"C minor"` | Musical key for generation | Any valid key (e.g., "C major", "F# minor", "Bb major") |
| `bpm` | number | `120` | Tempo in beats per minute | 60-200 |
| `bars` | number | `8` | Number of bars to generate | 1-64 |
| `instrument` | string | `"auto"` | GM instrument to use | GM instrument name or `"auto"` for layer default |
| `genre` | string | `"general"` | Musical genre/style | Any genre (e.g., "jazz", "rock", "classical", "electronic") |
| `renderAudio` | boolean | `true` | Whether to generate audio (WAV) or just MIDI | `true` \| `false` |

### Layer-Specific Defaults

| Layer | Default Instrument |
|-------|-------------------|
| `melody` | Acoustic Grand Piano |
| `bass` | Electric Bass Finger |
| `drums` | Standard Drum Kit |
| `chords` | Acoustic Grand Piano |

### Musical Keys

**Popular Major Keys:**
- C major, G major, D major, A major, E major, F major

**Popular Minor Keys:**
- A minor, E minor, B minor, D minor, G minor, F# minor

**Character Keys:**
- Bb major, Eb major, Ab major, C# minor, F minor, Bb minor

**Custom Keys:**
You can specify any key using standard notation: "C# major", "Db minor", etc.

### Tempo Guidelines

| Range | Description | Example Genres |
|-------|-------------|----------------|
| 60-80 BPM | Slow Ballad | Slow jazz, ballads |
| 90-120 BPM | Medium | Pop, rock, folk |
| 130-150 BPM | Upbeat | Dance, upbeat rock |
| 160-180 BPM | Fast | Electronic, metal |

### Instrument Categories

- **Piano**: acoustic_grand_piano, electric_piano_1, harpsichord
- **Guitar**: acoustic_guitar_steel, electric_guitar_clean, overdriven_guitar
- **Bass**: acoustic_bass, electric_bass_finger, slap_bass_1
- **Strings**: violin, viola, cello, contrabass
- **Brass**: trumpet, trombone, tuba, french_horn
- **Woodwinds**: flute, clarinet, saxophone, oboe
- **Synth**: lead_1_square, pad_1_new_age, synth_bass_1

[See `/instruments/categories` endpoint for complete list]

### Genre Examples

**Popular Genres:**
- `"jazz"` - Sophisticated harmony, swing rhythms, blue notes
- `"rock"` - Power chords, driving rhythms, strong beats
- `"classical"` - Traditional harmony, counterpoint, voice leading
- `"electronic"` - Synthetic textures, sequence patterns, modern rhythms
- `"blues"` - 12-bar progressions, blue notes, shuffle feel
- `"folk"` - Simple melodies, acoustic feel, traditional progressions
- `"latin"` - Clave rhythms, syncopation, Latin progressions
- `"country"` - Simple progressions, storytelling melodies

**Custom Genres:**
You can be specific: `"bossa nova"`, `"death metal"`, `"ambient"`, `"country blues"`

---

## Examples

### 1. Generate Jazz Melody (Stream Audio)

```bash
curl -X POST http://localhost:3001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "layer": "melody",
    "key": "F major",
    "bpm": 120,
    "bars": 16,
    "instrument": "acoustic_grand_piano",
    "genre": "jazz",
    "renderAudio": true
  }' \
  -o jazz_melody.wav
```

### 2. Generate Rock Bass (Stream MIDI)

```bash
curl -X POST http://localhost:3001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "layer": "bass",
    "key": "E minor",
    "bpm": 140,
    "bars": 8,
    "instrument": "electric_bass_finger",
    "genre": "rock",
    "renderAudio": false
  }' \
  -o rock_bass.mid
```

### 3. Generate Classical Strings (Stream Audio)

```bash
curl -X POST http://localhost:3001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "layer": "melody",
    "key": "D major",
    "bpm": 90,
    "bars": 12,
    "instrument": "violin",
    "genre": "classical",
    "renderAudio": true
  }' \
  -o classical_strings.wav
```

### 4. Generate Electronic Drums (Default Parameters)

```bash
curl -X POST http://localhost:3001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "layer": "drums",
    "genre": "electronic"
  }' \
  -o electronic_drums.wav
```

### 5. Async Generation for Long Pieces

```bash
# Start generation
JOB_ID=$(curl -s -X POST http://localhost:3001/api/generate/async \
  -H "Content-Type: application/json" \
  -d '{
    "layer": "chords",
    "key": "Bb major",
    "bpm": 100,
    "bars": 32,
    "genre": "jazz"
  }' | jq -r '.data.id')

# Check status
curl http://localhost:3001/api/generate/status/$JOB_ID

# Download when complete
curl http://localhost:3001/api/generate/download/$JOB_ID/audio -o long_chords.wav
```

### 6. JavaScript/Fetch Example

```javascript
const response = await fetch('http://localhost:3001/api/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    layer: 'melody',
    key: 'C major',
    bpm: 120,
    bars: 8,
    instrument: 'acoustic_grand_piano',
    genre: 'pop',
    renderAudio: true
  })
});

if (response.ok) {
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'generated_melody.wav';
  a.click();
}
```

### 7. Python Example

```python
import requests

response = requests.post('http://localhost:3001/api/generate', 
  json={
    'layer': 'bass',
    'key': 'G minor',
    'bpm': 110,
    'bars': 4,
    'instrument': 'synth_bass_1',
    'genre': 'electronic',
    'renderAudio': True
  }
)

if response.ok:
    with open('synth_bass.wav', 'wb') as f:
        f.write(response.content)
```

### 8. Postman Example

**Your Request (Fixed):**
```json
{
  "layer": "melody",
  "key": "F major",
  "bpm": 120,
  "bars": 8,
  "instrument": "Honky Tonk Piano",
  "genre": "dark, trap, hip hop",
  "renderAudio": true
}
```

**Postman Setup:**
1. **Method**: POST
2. **URL**: `http://localhost:3001/api/generate`
3. **Headers**: 
   - `Content-Type: application/json`
4. **Body**: Raw JSON (see above)
5. **Save Response**: Check "Send and Download" to save the audio/MIDI file

**Expected Response**: 
- WAV audio file with filename like `cosmic_wave_melody.wav`
- Headers include generation metadata in `X-Generation-Info`

**Common Postman Issues:**
- ❌ **Error**: "unrecognized arguments: tonk piano"
- ✅ **Fix**: API now auto-normalizes "Honkey tonk piano" → "honky_tonk_piano"
- 💡 **Tip**: Use `/instruments/categories` to see exact instrument names

---

## Error Handling

### HTTP Status Codes

- `200 OK` - Successful file stream
- `400 Bad Request` - Invalid parameters
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Generation failed
- `503 Engine Unavailable` - Conductio engine unavailable

### Error Response Format

```json
{
  "success": false,
  "error": "Invalid layer",
  "message": "Layer must be one of: melody, bass, drums, chords"
}
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid layer" | Layer not in allowed values | Use: melody, bass, drums, or chords |
| "Generation failed" | Conductio engine error | Check conductio engine logs, try again |
| "Service unavailable" | Conductio engine down | Ensure Python service is running |
| "Invalid instrument" | Unknown instrument name | Check `/instruments` endpoint |
| "unrecognized arguments" | Instrument name with spaces not quoted | Use underscore format: "honky_tonk_piano" |

### Instrument Name Formats

The API accepts instrument names in multiple formats and automatically normalizes them:

**✅ Recommended Format (underscore_case):**
```json
{
  "instrument": "honky_tonk_piano"
}
```

**✅ Also Accepted (space-separated, auto-normalized):**
```json
{
  "instrument": "Honky Tonk Piano"
}
```

**✅ Common Corrections Applied:**
- "Honkey tonk piano" → "honky_tonk_piano" 
- "Piano" → "acoustic_grand_piano"
- "Guitar" → "acoustic_guitar_steel"
- "Bass" → "electric_bass_finger"

**💡 Postman Tips:**
- Use exact instrument names from `/instruments` endpoint for best results
- Spaces and capitalization are automatically handled
- Check the response headers for normalized instrument name used

---

## Rate Limiting

Currently no rate limiting is implemented. For production use, implement appropriate rate limiting based on your needs.

---

## File Output

### Naming Convention

Generated files use creative naming: `{adjective}_{noun}_{layer}.{ext}`

**Examples:**
- `cosmic_wave_melody.wav`
- `golden_river_bass.mid`
- `mystic_thunder_drums.wav`

### File Formats

- **MIDI**: `.mid` - Standard MIDI format, compatible with all DAWs
- **Audio**: `.wav` - High-quality WAV audio, 44.1kHz/16-bit

### Generation Info Header

Audio/MIDI responses include an `X-Generation-Info` header with metadata:

```json
{
  "layer": "melody",
  "genre": "jazz",
  "key": "F major",
  "bpm": 120,
  "bars": 8,
  "instrument": "acoustic_grand_piano",
  "fileType": "wav",
  "createdAt": "2025-11-07T13-45-00-000Z"
}
```

---

## Testing

Use the included test script to verify API functionality:

```bash
chmod +x test-api.sh
./test-api.sh
```

This will test all endpoints and generate sample files.

---

## Support

For issues or questions:
1. Check the health endpoint: `GET /api/health`
2. Verify the Conductio Python engine is running
3. Check the API logs for error details
4. Ensure all required dependencies are installed

---

**Version**: 1.0.0  
**Last Updated**: November 7, 2025