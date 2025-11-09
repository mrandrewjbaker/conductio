# Conductio Documentation

## Overview

**Conductio** is an AI-powered music generation system that creates musical patterns and renders them as both MIDI and audio files. It focuses on musical structure (key, tempo, bars) rather than genre-specific styling, making it a versatile tool for composers and musicians.

## System Architecture

### Core Philosophy
- **AI-First**: Uses OpenAI GPT-4o-mini for intelligent pattern generation
- **Genre-Free**: Focuses on musical coherence rather than style presets
- **Layer-Based**: Generates individual musical layers (melody, drums, bass, chords)
- **Multi-Format Output**: Produces JSON patterns, MIDI files, and WAV audio

### Directory Structure
```
conductio-service/
├── main.py                 # CLI entry point
├── ai/                     # AI generation modules
│   ├── client.py           # OpenAI API interface
│   ├── prompt_builder.py   # Prompt construction
│   └── pattern_parser.py   # Response validation
├── generation/             # Output generation modules
│   ├── layer_runner.py     # Main generation orchestrator
│   ├── midi_builder.py     # MIDI file creation
│   └── audio_renderer.py   # WAV audio rendering
├── output/                 # Generated files (created automatically)
├── venv/                   # Python virtual environment
└── .env                    # Environment variables (API keys)
```

### Installation & Setup

### 1. Environment Setup
```bash
cd conductio-service
python3 -m venv venv
source venv/bin/activate
pip install openai mido python-dotenv pretty_midi soundfile numpy pyfluidsynth
```

### 2. Soundfont Setup
Ensure the FluidR3 soundfont is in place:
```bash
ls soundfonts/FluidR3_GM/FluidR3_GM.sf2
# Should show the FluidR3 soundfont file (~148MB)
```

### 3. API Key Configuration
Create a `.env` file in the `conductio-service` directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Verify Installation
```bash
python main.py --layer melody --bars 4 --no-audio
```

## Usage

### Basic Command Structure
```bash
python main.py --layer LAYER [OPTIONS]
```

### Parameters

| Parameter | Required | Description | Default | Options |
|-----------|----------|-------------|---------|---------|
| `--layer` | ✅ | Type of musical layer to generate | - | `melody`, `drums`, `bass`, `chords` |
| `--key` | ❌ | Musical key for the composition | `"C minor"` | Any valid key (e.g., `"F major"`, `"A# minor"`) |
| `--bpm` | ❌ | Tempo in beats per minute | `120` | Any integer (typically 60-200) |
| `--bars` | ❌ | Length in musical bars | `8` | Any integer (typically 1-32) |
| `--no-audio` | ❌ | Skip audio rendering (MIDI only) | `false` | Flag (no value needed) |

## Examples

### Basic Layer Generation

#### 1. Simple Melody
```bash
python main.py --layer melody
```
**Output:**
- Creates a 8-bar melody in C minor at 120 BPM
- Generates: `pattern.json`, `melody.mid`, `melody.wav`

#### 2. Custom Key and Tempo
```bash
python main.py --layer melody --key "G major" --bpm 140 --bars 16
```
**Output:**
- Creates a 16-bar melody in G major at 140 BPM
- More energetic, longer composition

#### 3. Bass Line
```bash
python main.py --layer bass --key "E minor" --bpm 80 --bars 4
```
**Output:**
- Creates a 4-bar bass pattern in E minor at 80 BPM
- Uses appropriate bass instrument synthesis

#### 4. Drum Pattern
```bash
python main.py --layer drums --bpm 110 --bars 8
```
**Output:**
- Creates an 8-bar drum pattern at 110 BPM
- Key parameter ignored for drums (rhythm-only)

#### 5. Chord Progression
```bash
python main.py --layer chords --key "F major" --bars 12
```
**Output:**
- Creates a 12-bar chord progression in F major
- Uses piano synthesis for harmonic content

### Advanced Usage

#### 6. MIDI-Only Generation (No Audio)
```bash
python main.py --layer melody --key "D minor" --no-audio
```
**Output:**
- Skips audio rendering for faster generation
- Only creates `pattern.json` and `melody.mid`

#### 7. Short Loop Creation
```bash
python main.py --layer drums --bpm 128 --bars 2
```
**Output:**
- Creates a 2-bar drum loop perfect for repetition
- Higher BPM suitable for electronic music

#### 8. Slow Ballad Bass
```bash
python main.py --layer bass --key "A minor" --bpm 60 --bars 32
```
**Output:**
- Creates a long, slow bass line for ballads
- Extended length for full song sections

## Output Structure

Each generation creates a timestamped directory:
```
output/
└── 20251106_193444_bass/
    ├── pattern.json    # Structured musical data
    ├── bass.mid        # MIDI file
    └── bass.wav        # Audio file (if rendered)
```

### Pattern JSON Format
```json
{
  "metadata": {
    "layer": "melody",
    "bpm": 120,
    "key": "C minor",
    "bars": 8
  },
  "pattern": [
    {
      "note": 60,         # MIDI note number (C4)
      "velocity": 90,     # Note velocity (0-127)
      "duration": 480,    # Duration in MIDI ticks
      "bar": 1,           # Which bar (1-indexed)
      "beat": 1.0         # Beat position within bar
    }
  ]
}
```

### Musical Layer Types

### Melody
- **Instrument**: Acoustic Piano (FluidR3 GM Program 0)
- **Range**: Typically C4-C6 (60-84)
- **Focus**: Singable melodic lines with musical phrases

### Bass
- **Instrument**: Acoustic Bass (FluidR3 GM Program 32)
- **Range**: Typically E1-G3 (28-55)  
- **Focus**: Root notes, walking bass lines, rhythmic foundation

### Drums
- **Instrument**: Standard Drum Kit (FluidR3 GM Channel 9)
- **Notes**: Standard GM drum mapping (kick=36, snare=38, hihat=42, etc.)
- **Focus**: Rhythmic patterns, groove, percussion

### Chords
- **Instrument**: Acoustic Piano (FluidR3 GM Program 0)
- **Range**: Typically C3-C5 (48-72)
- **Focus**: Harmonic progressions, chord voicings, accompaniment

## Workflow Examples

### Creating a Complete Song Structure

#### 1. Generate Bass Foundation
```bash
python main.py --layer bass --key "Am" --bpm 95 --bars 8
```

#### 2. Add Drum Groove
```bash
python main.py --layer drums --bpm 95 --bars 8
```

#### 3. Create Chord Progression  
```bash
python main.py --layer chords --key "Am" --bpm 95 --bars 8
```

#### 4. Add Melody
```bash
python main.py --layer melody --key "Am" --bpm 95 --bars 8
```

### Creating Variations

#### Theme and Variations
```bash
# Main theme
python main.py --layer melody --key "C major" --bars 8

# Variation 1: Different key
python main.py --layer melody --key "A minor" --bars 8  

# Variation 2: Different tempo
python main.py --layer melody --key "C major" --bpm 140 --bars 8

# Variation 3: Extended length
python main.py --layer melody --key "C major" --bars 16
```

## Technical Details

### AI Generation Process
1. **Prompt Construction**: Musical parameters converted to natural language prompt
2. **API Call**: OpenAI GPT-4o-mini generates JSON pattern
3. **Validation**: Response validated against Conductio schema
4. **MIDI Conversion**: Pattern converted to MIDI events
5. **Audio Rendering**: MIDI synthesized to WAV using FluidR3 soundfont via FluidSynth

### Audio Synthesis
- **Soundfont**: FluidR3 General MIDI soundfont for high-quality instrument synthesis
- **Sample Rate**: 44.1kHz (CD quality)
- **Synthesis Engine**: 
  - Melodic instruments: FluidSynth with FluidR3 soundfont
  - Drums: pretty_midi synthesis (more reliable for percussion)
  - Automatic fallback to pretty_midi if FluidSynth fails
- **Instruments**: Full GM-compatible instrument set (128 instruments + drum kits)
- **Normalization**: Audio normalized to prevent clipping (-0.8 dBFS)
- **Format**: 16-bit WAV files

### Error Handling
- **API Failures**: Graceful degradation with informative error messages
- **Missing API Key**: Automatic fallback to mock patterns for testing
- **Audio Errors**: Continues with MIDI generation if audio rendering fails

## Troubleshooting

### Common Issues

#### "No OPENAI_API_KEY found"
- **Solution**: Create `.env` file with your OpenAI API key
- **Test**: Set `export OPENAI_API_KEY=your_key` in terminal

#### Audio rendering warnings
- **Cause**: Pretty_midi synthesis limitations with certain patterns
- **Impact**: Audio still generates successfully
- **Solution**: Warnings are cosmetic and can be ignored

#### Empty MIDI files
- **Cause**: AI generated invalid or empty patterns
- **Solution**: Try regenerating with different parameters

### Performance Tips
- Use `--no-audio` for faster iteration during development
- Shorter `--bars` values generate faster
- Lower `--bpm` values may produce more musical results

## Future Enhancements

### Planned Features
- **Soundfont Support**: Custom instrument libraries
- **Multi-layer Sessions**: Generate complete arrangements
- **Pattern Templates**: Pre-built musical structures
- **Export Formats**: Support for additional audio formats
- **Real-time Preview**: Live audio playback during generation

### Extensibility
The modular architecture makes it easy to add:
- New layer types (strings, synth, etc.)
- Custom synthesis engines
- Additional AI models
- Export formats (Ableton Live, FL Studio, etc.)

## API Reference

### Main Functions

#### `run_layer(layer, key, bpm, bars, render_audio_flag)`
Primary generation function that orchestrates the entire process.

#### `generate_pattern(prompt, model)`
Calls OpenAI API with musical prompt and returns structured JSON.

#### `build_midi(pattern, output_path)`
Converts pattern JSON to MIDI file.

#### `render_audio(midi_path, output_dir, layer_type)`
Synthesizes MIDI to WAV audio file.

---

*Conductio - AI-Powered Music Generation System*