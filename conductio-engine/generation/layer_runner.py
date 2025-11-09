from ai.prompt_builder import build_prompt
from ai.client import generate_pattern
from ai.pattern_parser import validate_pattern
from generation.midi_builder import build_midi
from generation.audio_renderer import render_audio
from generation.instruments import get_instrument_program, get_default_instrument_for_layer
from pathlib import Path
import json, time, random

def generate_creative_name() -> str:
    """Generate a creative adjective + noun combination for output folder names."""
    adjectives = [
        "cosmic", "electric", "golden", "silver", "mystic", "velvet", "crystal", "shadow",
        "bright", "deep", "smooth", "wild", "serene", "fierce", "gentle", "bold",
        "dreamy", "crisp", "warm", "cool", "rich", "pure", "subtle", "vivid",
        "flowing", "dancing", "soaring", "glowing", "shimmering", "resonant", "harmonic", "melodic"
    ]
    
    nouns = [
        "wave", "echo", "pulse", "flow", "spark", "dream", "storm", "breeze",
        "river", "mountain", "ocean", "forest", "sky", "star", "moon", "sun",
        "bridge", "journey", "path", "garden", "valley", "peak", "canyon", "meadow",
        "whisper", "thunder", "lightning", "rainbow", "mist", "aurora", "cascade", "symphony"
    ]
    
    return f"{random.choice(adjectives)}_{random.choice(nouns)}"

def run_layer(layer: str, key: str, bpm: int, bars: int, instrument: str = "auto", render_audio_flag: bool = True, genre: str = "general"):
    """Run a single-layer AI generation (melody, drums, etc.)."""
    
    # Resolve instrument
    if instrument == "auto":
        instrument_program = get_default_instrument_for_layer(layer)
        instrument_name = "default"
    else:
        try:
            instrument_program = get_instrument_program(instrument)
            instrument_name = instrument
        except ValueError as e:
            print(f"❌ {e}")
            return
    
    prompt = build_prompt(layer, key, bpm, bars, instrument_name if instrument_name != "default" else "piano", genre)
    print(f"🧠 Generating {layer} layer with GPT-5-mini…")
    if instrument_name != "default":
        print(f"🎵 Using instrument: {instrument_name} (GM Program {instrument_program})")
    
    ai_data = generate_pattern(prompt, layer=layer, key=key, bpm=bpm, bars=bars)
    pattern = validate_pattern(ai_data)

    # session folder with creative naming
    creative_name = generate_creative_name()
    outdir = Path("output") / f"{creative_name}_{layer}.mcpkg"
    outdir.mkdir(parents=True, exist_ok=True)

    # save pattern
    json.dump(pattern, open(outdir / "pattern.json", "w"), indent=2)
    midi_path = outdir / f"{layer}.mid"
    build_midi(pattern["pattern"], midi_path, layer, instrument_program)
    print(f"✅ Saved {layer} MIDI to {midi_path}")
    
    # render audio if requested
    if render_audio_flag:
        wav_path = render_audio(midi_path, outdir, layer, instrument_program)
        if wav_path:
            print(f"🎶 Audio rendering complete!")
        else:
            print(f"⚠️  Audio rendering failed, MIDI file still available")