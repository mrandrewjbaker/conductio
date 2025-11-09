# Conductio API

REST API server for the Conductio AI Music Generation System. This Express.js/TypeScript API provides HTTP endpoints to interact with the Python-based Conductio service.

## Features

- 🎵 **Music Generation**: Generate melody, bass, drums, and chord layers
- 🎼 **Instrument Support**: Access to 128 General MIDI instruments
- 🎨 **Genre-Aware**: AI prompts adapted for different musical genres
- 📁 **File Management**: Download generated MIDI and audio files
- 💾 **Job Tracking**: Asynchronous generation with status monitoring
- 🔍 **Health Checks**: Service availability monitoring

## API Endpoints

### Health & Info
- `GET /api/health` - Health check and service status
- `GET /api/health/info` - API documentation and examples

### Music Generation
- `POST /api/generate` - Start music generation
- `GET /api/generate/status/:id` - Check generation status
- `GET /api/generate/download/:id/:type` - Download files (midi/audio)

### Instruments
- `GET /api/instruments` - List all available instruments
- `GET /api/instruments/categories` - List instruments by category

## Quick Start

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env if needed
   ```

3. **Build & Start**
   ```bash
   # Development mode with auto-restart
   npm run dev
   
   # Production build and start
   npm run build
   npm start
   ```

4. **Verify Installation**
   ```bash
   curl http://localhost:3001/api/health
   ```

## Usage Examples

### Stream a Jazz Melody (New!)
```bash
curl -X POST http://localhost:3001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "layer": "melody",
    "key": "F major",
    "bpm": 120,
    "bars": 8,
    "instrument": "acoustic_grand_piano",
    "genre": "jazz",
    "renderAudio": true
  }' \
  -o jazz_melody.wav
```

### Stream a Rock Bass MIDI
```bash
curl -X POST http://localhost:3001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "layer": "bass",
    "key": "E minor", 
    "bpm": 140,
    "genre": "rock",
    "renderAudio": false
  }' \
  -o rock_bass.mid
```

### List Available Instruments
```bash
curl http://localhost:3001/api/instruments/categories
```

**📖 For complete documentation with all parameters, examples, and advanced usage, see [DOCS.md](./DOCS.md)**

## API Response Format

All endpoints return JSON responses in this format:

```json
{
  "success": true|false,
  "data": { ... },
  "error": "error type (if applicable)",
  "message": "detailed message (if applicable)"
}
```

## Generation Request Format

```typescript
interface GenerationRequest {
  layer: 'melody' | 'bass' | 'drums' | 'chords';
  key?: string;           // Default: "C minor"
  bpm?: number;           // Default: 120
  bars?: number;          // Default: 8
  instrument?: string;    // Default: "auto"
  genre?: string;         // Default: "general"
  renderAudio?: boolean;  // Default: true
}
```

## Development

### Project Structure
```
src/
├── index.ts              # Main server file
├── types/               # TypeScript type definitions
├── routes/              # API route handlers
│   ├── health.ts        # Health check endpoints
│   ├── generation.ts    # Music generation endpoints
│   └── instruments.ts   # Instrument listing endpoints
└── services/            # Business logic
    └── conductioService.ts  # Python service wrapper
```

### Available Scripts
- `npm run dev` - Development mode with hot reload
- `npm run build` - Build TypeScript to JavaScript
- `npm run start` - Start production server
- `npm run clean` - Clean build directory

## Requirements

- Node.js 18+
- Conductio Python service (in sibling directory)
- Python 3.13+ with virtual environment

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `3001` | Server port |
| `NODE_ENV` | `development` | Environment mode |
| `CONDUCTIO_SERVICE_PATH` | `../conductio-service` | Path to Python service |
| `PYTHON_CMD` | `./venv/bin/python` | Python executable command |
| `CORS_ORIGIN` | `http://localhost:3000` | CORS allowed origin |

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input parameters
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Service errors
- **503 Service Unavailable**: Conductio service unavailable

## License

MIT License - see LICENSE file for details.