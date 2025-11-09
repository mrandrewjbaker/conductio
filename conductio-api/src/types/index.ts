export interface GenerationRequest {
  layer: 'melody' | 'bass' | 'drums' | 'chords';
  key?: string;
  bpm?: number;
  bars?: number;
  instrument?: string;
  genre?: string;
  renderAudio?: boolean;
}

export interface GenerationResponse {
  success: boolean;
  data?: {
    id: string;
    layer: string;
    genre: string;
    key: string;
    bpm: number;
    bars: number;
    instrument: string;
    outputPath: string;
    midiFile: string;
    audioFile?: string;
    createdAt: string;
  };
  error?: string;
  message?: string;
}

export interface Instrument {
  id: number;
  name: string;
  displayName: string;
  category: string;
}

export interface InstrumentCategory {
  name: string;
  instruments: Instrument[];
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  uptime: number;
  version: string;
  services: {
    conductioService: 'available' | 'unavailable';
    python: 'available' | 'unavailable';
  };
}