# General MIDI Instrument Mappings for FluidR3
# Program numbers are 0-indexed (subtract 1 from standard GM numbers)

GM_INSTRUMENTS = {
    # Piano Family (0-7)
    "acoustic_grand_piano": 0,
    "bright_acoustic_piano": 1,
    "electric_grand_piano": 2,
    "honky_tonk_piano": 3,
    "electric_piano_1": 4,
    "electric_piano_2": 5,
    "harpsichord": 6,
    "clavinet": 7,
    
    # Chromatic Percussion (8-15)
    "celesta": 8,
    "glockenspiel": 9,
    "music_box": 10,
    "vibraphone": 11,
    "marimba": 12,
    "xylophone": 13,
    "tubular_bells": 14,
    "dulcimer": 15,
    
    # Organ (16-23)
    "drawbar_organ": 16,
    "percussive_organ": 17,
    "rock_organ": 18,
    "church_organ": 19,
    "reed_organ": 20,
    "accordion": 21,
    "harmonica": 22,
    "tango_accordion": 23,
    
    # Guitar (24-31)
    "acoustic_guitar_nylon": 24,
    "acoustic_guitar_steel": 25,
    "electric_guitar_jazz": 26,
    "electric_guitar_clean": 27,
    "electric_guitar_muted": 28,
    "overdriven_guitar": 29,
    "distortion_guitar": 30,
    "guitar_harmonics": 31,
    
    # Bass (32-39)
    "acoustic_bass": 32,
    "electric_bass_finger": 33,
    "electric_bass_pick": 34,
    "fretless_bass": 35,
    "slap_bass_1": 36,
    "slap_bass_2": 37,
    "synth_bass_1": 38,
    "synth_bass_2": 39,
    
    # Strings (40-47)
    "violin": 40,
    "viola": 41,
    "cello": 42,
    "contrabass": 43,
    "tremolo_strings": 44,
    "pizzicato_strings": 45,
    "orchestral_harp": 46,
    "timpani": 47,
    
    # Ensemble (48-55)
    "string_ensemble_1": 48,
    "string_ensemble_2": 49,
    "synth_strings_1": 50,
    "synth_strings_2": 51,
    "choir_aahs": 52,
    "voice_oohs": 53,
    "synth_voice": 54,
    "orchestra_hit": 55,
    
    # Brass (56-63)
    "trumpet": 56,
    "trombone": 57,
    "tuba": 58,
    "muted_trumpet": 59,
    "french_horn": 60,
    "brass_section": 61,
    "synth_brass_1": 62,
    "synth_brass_2": 63,
    
    # Reed (64-71)
    "soprano_sax": 64,
    "alto_sax": 65,
    "tenor_sax": 66,
    "baritone_sax": 67,
    "oboe": 68,
    "english_horn": 69,
    "bassoon": 70,
    "clarinet": 71,
    
    # Pipe (72-79)
    "piccolo": 72,
    "flute": 73,
    "recorder": 74,
    "pan_flute": 75,
    "blown_bottle": 76,
    "shakuhachi": 77,
    "whistle": 78,
    "ocarina": 79,
    
    # Synth Lead (80-87)
    "lead_1_square": 80,
    "lead_2_sawtooth": 81,
    "lead_3_calliope": 82,
    "lead_4_chiff": 83,
    "lead_5_charang": 84,
    "lead_6_voice": 85,
    "lead_7_fifths": 86,
    "lead_8_bass_lead": 87,
    
    # Synth Pad (88-95)
    "pad_1_new_age": 88,
    "pad_2_warm": 89,
    "pad_3_polysynth": 90,
    "pad_4_choir": 91,
    "pad_5_bowed": 92,
    "pad_6_metallic": 93,
    "pad_7_halo": 94,
    "pad_8_sweep": 95,
    
    # Synth Effects (96-103)
    "fx_1_rain": 96,
    "fx_2_soundtrack": 97,
    "fx_3_crystal": 98,
    "fx_4_atmosphere": 99,
    "fx_5_brightness": 100,
    "fx_6_goblins": 101,
    "fx_7_echoes": 102,
    "fx_8_sci_fi": 103,
    
    # Ethnic (104-111)
    "sitar": 104,
    "banjo": 105,
    "shamisen": 106,
    "koto": 107,
    "kalimba": 108,
    "bag_pipe": 109,
    "fiddle": 110,
    "shanai": 111,
    
    # Percussive (112-119)
    "tinkle_bell": 112,
    "agogo": 113,
    "steel_drums": 114,
    "woodblock": 115,
    "taiko_drum": 116,
    "melodic_tom": 117,
    "synth_drum": 118,
    "reverse_cymbal": 119,
    
    # Sound Effects (120-127)
    "guitar_fret_noise": 120,
    "breath_noise": 121,
    "seashore": 122,
    "bird_tweet": 123,
    "telephone_ring": 124,
    "helicopter": 125,
    "applause": 126,
    "gunshot": 127,
}

# Common aliases for easier use
INSTRUMENT_ALIASES = {
    # Piano aliases
    "piano": 0,
    "grand_piano": 0,
    "electric_piano": 4,
    "ep": 4,
    
    # Guitar aliases  
    "guitar": 25,
    "acoustic_guitar": 25,
    "electric_guitar": 27,
    "clean_guitar": 27,
    "jazz_guitar": 26,
    "rock_guitar": 29,
    "lead_guitar": 29,
    
    # Bass aliases
    "bass": 32,
    "electric_bass": 33,
    "upright_bass": 32,
    "synth_bass": 38,
    
    # Strings aliases
    "strings": 48,
    "orchestra": 48,
    "choir": 52,
    
    # Brass aliases
    "horn": 60,
    "brass": 61,
    
    # Woodwinds aliases
    "sax": 65,
    "saxophone": 65,
    
    # Synth aliases
    "synth": 81,
    "lead": 81,
    "pad": 89,
}

def get_instrument_program(instrument_name: str) -> int:
    """
    Get GM program number for an instrument name.
    
    Args:
        instrument_name: Name or number of instrument
        
    Returns:
        GM program number (0-127)
        
    Raises:
        ValueError: If instrument not found
    """
    # Handle numeric input
    if instrument_name.isdigit():
        program = int(instrument_name)
        if 0 <= program <= 127:
            return program
        else:
            raise ValueError(f"Program number must be 0-127, got {program}")
    
    # Convert to lowercase and replace spaces/hyphens with underscores
    name = instrument_name.lower().replace(" ", "_").replace("-", "_")
    
    # Check main instruments dict
    if name in GM_INSTRUMENTS:
        return GM_INSTRUMENTS[name]
    
    # Check aliases
    if name in INSTRUMENT_ALIASES:
        return INSTRUMENT_ALIASES[name]
    
    # If not found, suggest close matches
    similar = [k for k in list(GM_INSTRUMENTS.keys()) + list(INSTRUMENT_ALIASES.keys()) 
               if name in k or k in name]
    
    if similar:
        raise ValueError(f"Instrument '{instrument_name}' not found. Did you mean: {', '.join(similar[:5])}?")
    else:
        raise ValueError(f"Instrument '{instrument_name}' not found. Use --list-instruments to see available instruments.")

def get_default_instrument_for_layer(layer: str) -> int:
    """Get default instrument program for a layer type."""
    defaults = {
        "melody": 0,    # Acoustic Grand Piano
        "bass": 32,     # Acoustic Bass
        "chords": 0,    # Acoustic Grand Piano
        "drums": 0,     # Drums use channel 9, program doesn't matter
    }
    return defaults.get(layer, 0)

def list_instruments_by_category():
    """Return instruments organized by category for help display."""
    categories = {
        "Piano": [(k, v) for k, v in GM_INSTRUMENTS.items() if 0 <= v <= 7],
        "Guitar": [(k, v) for k, v in GM_INSTRUMENTS.items() if 24 <= v <= 31],
        "Bass": [(k, v) for k, v in GM_INSTRUMENTS.items() if 32 <= v <= 39],
        "Strings": [(k, v) for k, v in GM_INSTRUMENTS.items() if 40 <= v <= 47],
        "Brass": [(k, v) for k, v in GM_INSTRUMENTS.items() if 56 <= v <= 63],
        "Woodwinds": [(k, v) for k, v in GM_INSTRUMENTS.items() if 64 <= v <= 79],
        "Synth": [(k, v) for k, v in GM_INSTRUMENTS.items() if 80 <= v <= 95],
        "Popular": [
            ("acoustic_grand_piano", GM_INSTRUMENTS["acoustic_grand_piano"]),
            ("electric_piano_1", GM_INSTRUMENTS["electric_piano_1"]),
            ("acoustic_guitar_steel", GM_INSTRUMENTS["acoustic_guitar_steel"]),
            ("electric_guitar_clean", GM_INSTRUMENTS["electric_guitar_clean"]),
            ("acoustic_bass", GM_INSTRUMENTS["acoustic_bass"]),
            ("electric_bass_finger", GM_INSTRUMENTS["electric_bass_finger"]),
            ("violin", GM_INSTRUMENTS["violin"]),
            ("trumpet", GM_INSTRUMENTS["trumpet"]),
            ("alto_sax", GM_INSTRUMENTS["alto_sax"]),
            ("flute", GM_INSTRUMENTS["flute"]),
        ]
    }
    return categories