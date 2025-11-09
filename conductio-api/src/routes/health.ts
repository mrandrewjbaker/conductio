import { Router } from 'express';
import { HealthStatus, ApiResponse } from '../types';
import { ConductioService } from '../services/conductioEngine';

const router = Router();

router.get('/', async (req, res) => {
  try {
    const startTime = Date.now();
    const uptime = process.uptime();
    
    // Check Conductio service availability
    const conductioAvailable = await ConductioService.checkAvailability();
    
    const healthStatus: HealthStatus = {
      status: conductioAvailable ? 'healthy' : 'degraded',
      timestamp: new Date().toISOString(),
      uptime: Math.floor(uptime),
      version: '1.0.0',
      services: {
        conductioService: conductioAvailable ? 'available' : 'unavailable',
        python: conductioAvailable ? 'available' : 'unavailable'
      }
    };

    const response: ApiResponse<HealthStatus> = {
      success: true,
      data: healthStatus
    };

    res.status(healthStatus.status === 'healthy' ? 200 : 503).json(response);
  } catch (error) {
    const errorResponse: ApiResponse = {
      success: false,
      error: 'Health check failed',
      message: error instanceof Error ? error.message : 'Unknown error'
    };
    res.status(500).json(errorResponse);
  }
});

router.get('/info', (req, res) => {
  const apiInfo = {
    name: 'Conductio API',
    version: '1.0.0',
    description: 'REST API for AI Music Generation',
    endpoints: {
      health: {
        'GET /api/health': 'Health check and service status',
        'GET /api/health/info': 'API information and documentation'
      },
      generation: {
        'POST /api/generate': 'Generate and stream music file directly (MIDI/WAV)',
        'POST /api/generate/async': 'Start async generation (returns job ID)',
        'GET /api/generate/status/:id': 'Get async generation status',
        'GET /api/generate/download/:id/:type': 'Download async generated files'
      },
      instruments: {
        'GET /api/instruments': 'List all available instruments',
        'GET /api/instruments/categories': 'List instruments by category'
      }
    },
    examples: {
      generateAndStreamAudio: {
        url: 'POST /api/generate',
        description: 'Generate and immediately stream audio file',
        body: {
          layer: 'melody',
          key: 'F major',
          bpm: 120,
          bars: 8,
          instrument: 'acoustic_grand_piano',
          genre: 'jazz',
          renderAudio: true
        },
        response: 'Streams WAV audio file directly'
      },
      generateAndStreamMIDI: {
        url: 'POST /api/generate',
        description: 'Generate and immediately stream MIDI file',
        body: {
          layer: 'bass',
          key: 'E minor',
          bpm: 140,
          bars: 4,
          instrument: 'electric_bass_finger',
          genre: 'rock',
          renderAudio: false
        },
        response: 'Streams MIDI file directly'
      }
    }
  };

  const response: ApiResponse = {
    success: true,
    data: apiInfo
  };

  res.json(response);
});

export { router as healthRoutes };