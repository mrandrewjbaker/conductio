import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';
import fs from 'fs/promises';
import { GenerationRequest } from '../types';

const execAsync = promisify(exec);

export class ConductioService {
  private static readonly CONDUCTIO_SERVICE_PATH = path.join(process.cwd(), '..', 'conductio-service');
  private static readonly PYTHON_CMD = './venv/bin/python';
  
  private static normalizeInstrumentName(instrument: string): string {
    // Handle common variations and normalize instrument names
    if (instrument === 'auto') return instrument;
    
    // Convert to lowercase and replace spaces/hyphens with underscores
    let normalized = instrument.toLowerCase()
      .replace(/[- ]+/g, '_')
      .replace(/[^a-z0-9_]/g, ''); // Remove special characters
    
    // Handle common misspellings/variations
    const corrections: Record<string, string> = {
      'honkey_tonk_piano': 'honky_tonk_piano',
      'honky_tonk': 'honky_tonk_piano',
      'piano': 'acoustic_grand_piano',
      'guitar': 'acoustic_guitar_steel',
      'bass': 'electric_bass_finger',
      'violin_1': 'violin',
      'strings': 'violin'
    };
    
    return corrections[normalized] || normalized;
  }
  
  static async checkAvailability(): Promise<boolean> {
    try {
      // Check if conductio-service directory exists
      await fs.access(this.CONDUCTIO_SERVICE_PATH);
      
      // Try to run a simple command to verify Python environment
      const { stdout } = await execAsync(`cd "${this.CONDUCTIO_SERVICE_PATH}" && ${this.PYTHON_CMD} --version`, {
        timeout: 5000
      });
      
      return stdout.includes('Python');
    } catch (error) {
      console.error('Conductio service availability check failed:', error);
      return false;
    }
  }
  
  static async generateLayer(request: GenerationRequest): Promise<{
    success: boolean;
    outputPath?: string;
    error?: string;
  }> {
    try {
      const {
        layer,
        key = 'C minor',
        bpm = 120,
        bars = 8,
        instrument = 'auto',
        genre = 'general',
        renderAudio = true
      } = request;
      
      // Normalize instrument name
      const normalizedInstrument = this.normalizeInstrumentName(instrument);
      
      // Build the command
      const args = [
        'main.py',
        '--layer', layer,
        '--key', `"${key}"`,
        '--bpm', bpm.toString(),
        '--bars', bars.toString(),
        '--instrument', `"${normalizedInstrument}"`,
        '--genre', `"${genre}"`
      ];
      
      if (!renderAudio) {
        args.push('--no-audio');
      }
      
      const cmd = `cd "${this.CONDUCTIO_SERVICE_PATH}" && ${this.PYTHON_CMD} ${args.join(' ')}`;
      console.log('Executing:', cmd);
      
      const { stdout, stderr } = await execAsync(cmd, {
        timeout: 240000, // 4 minute timeout (AI + audio rendering can take time)
        maxBuffer: 1024 * 1024 // 1MB buffer
      });
      
      console.log('Conductio output:', stdout);
      if (stderr) {
        console.error('Conductio stderr:', stderr);
      }
      
      // Parse output to find the generated folder
      const outputMatch = stdout.match(/✅ Saved \w+ MIDI to (output\/[^\/]+\.mcpkg)/);
      if (!outputMatch) {
        throw new Error('Could not parse output path from Conductio response');
      }
      
      const outputPath = outputMatch[1];
      
      return {
        success: true,
        outputPath: path.join(this.CONDUCTIO_SERVICE_PATH, outputPath)
      };
      
    } catch (error) {
      console.error('Layer generation failed:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }
  
  static async listInstruments(): Promise<{
    success: boolean;
    instruments?: any[];
    error?: string;
  }> {
    try {
      const cmd = `cd "${this.CONDUCTIO_SERVICE_PATH}" && ${this.PYTHON_CMD} -c "
from generation.instruments import list_instruments_by_category
import json
categories = list_instruments_by_category()
result = []
for category, instruments in categories.items():
    for name, program in instruments:
        result.append({
            'id': program,
            'name': name,
            'displayName': name.replace('_', ' ').title(),
            'category': category
        })
print(json.dumps(result))
"`;
      
      const { stdout, stderr } = await execAsync(cmd, { timeout: 10000 });
      
      if (stderr) {
        console.error('Instrument listing stderr:', stderr);
      }
      
      const instruments = JSON.parse(stdout.trim());
      
      return {
        success: true,
        instruments
      };
      
    } catch (error) {
      console.error('Instrument listing failed:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }
}