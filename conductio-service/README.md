# Conductio 🎵

> AI-Powered Music Generation System

Generate musical patterns using AI and render them as MIDI and audio files. Conductio focuses on musical structure over genre, creating coherent melodies, bass lines, drum patterns, and chord progressions.

## Quick Start

```bash
cd conductio-service
source venv/bin/activate
python main.py --layer melody --key "C major" --bpm 120 --bars 8
```

**Output:** `pattern.json`, `melody.mid`, `melody.wav`

## Features

🧠 **AI-Generated Patterns** - Uses OpenAI GPT-4o-mini for intelligent composition  
🎹 **Multi-Layer Support** - Generate melody, bass, drums, and chords separately  
🎼 **MIDI + Audio Output** - Creates both MIDI files and WAV audio  
🎵 **FluidR3 Soundfont** - High-quality General MIDI instrument synthesis  
🚀 **Genre-Free Approach** - Focuses on musical structure, not style presets  
⚡ **Fast Generation** - Typical pattern generated in 2-5 seconds  

## Layer Types

| Layer | Description | Example Use |
|-------|-------------|-------------|
| `melody` | Singable melodic lines | Lead melodies, hooks, themes |
| `bass` | Low-frequency foundation | Walking bass, root notes, grooves |
| `drums` | Rhythmic percussion | Beats, fills, percussion loops |
| `chords` | Harmonic progressions | Accompaniment, pads, progressions |

## Examples

```bash
# Quick melody in G major
python main.py --layer melody --key "G major" --bars 4

# Uptempo drum pattern  
python main.py --layer drums --bpm 140 --bars 2

# Slow bass line
python main.py --layer bass --key "A minor" --bpm 70 --bars 16

# Jazz chord progression
python main.py --layer chords --key "F major" --bars 12
```

## Documentation

See [DOCS.md](DOCS.md) for:
- Complete installation guide
- Detailed parameter reference  
- Workflow examples
- Technical architecture
- Troubleshooting guide

## Requirements

- Python 3.8+
- OpenAI API key
- ~50MB disk space for dependencies

## License

MIT License - See LICENSE file for details.

---

*Made with ♪ by the Conductio team*