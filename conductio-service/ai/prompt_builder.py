def build_prompt(layer: str, key: str, bpm: int, bars: int, instrument: str = "piano", genre: str = "general") -> str:
    """Construct an instruction prompt for AI generation."""
    
    # Get instrument-specific guidance
    instrument_guidance = get_instrument_guidance(layer, instrument)
    
    return f"""
You are an expert music pattern composer.
Generate a {bars}-bar {layer} pattern for {instrument} in {key} at {bpm} BPM in {genre} style.
Focus on musical coherence and playability for this specific instrument and genre.

{instrument_guidance}

Return ONLY valid JSON in this format:
{{
  "metadata": {{
    "layer": "{layer}",
    "bpm": {bpm},
    "key": "{key}",
    "bars": {bars},
    "instrument": "{instrument}",
    "genre": "{genre}"
  }},
  "pattern": [
    {{
      "note": 55,
      "velocity": 90,
      "duration": 480,
      "bar": 1,
      "beat": 1.0
    }},
    {{
      "note": 58,
      "velocity": 90,
      "duration": 480,
      "bar": 1,
      "beat": 1.0
    }}
  ]
}}

------
weirdness: 50%
variability: 70%

"""

def get_instrument_guidance(layer: str, instrument: str) -> str:
    """Get instrument-specific composition guidance."""
    
    # Normalize instrument name for matching
    inst_lower = instrument.lower().replace("_", " ").replace("-", " ")
    
    # Guitar family guidance
    if any(word in inst_lower for word in ["guitar", "bass"]):
        if "bass" in inst_lower:
            return """
BASS INSTRUMENT GUIDELINES:

- Emphasize root notes and fifth intervals
- Create rhythmic foundation with steady patterns
- Use techniques like walking bass lines or syncopated rhythms
- Velocity range 70-110 for consistent bass presence
"""
        else:
            return """
GUITAR INSTRUMENT GUIDELINES:
- Use guitar-friendly keys and chord shapes
- Create patterns that work with guitar fingering
- Use realistic note ranges: E2-E5 (MIDI 40-76)
- Include chord tones and passing notes
- Velocity range 60-120 for dynamic expression
"""
    
    # Piano family guidance
    elif any(word in inst_lower for word in ["piano", "keyboard", "harpsichord"]):
        return """
PIANO INSTRUMENT GUIDELINES:
- Full keyboard range available: A0-C8 (MIDI 21-108)
- Create flowing melodic lines or rich harmonic patterns
- Use piano-specific techniques like arpeggios, scales, or chord voicings
- Balance between melody and harmony as appropriate for the layer
- Velocity range 40-127 for full dynamic expression
"""
    
    # String instruments guidance
    elif any(word in inst_lower for word in ["violin", "viola", "cello", "strings"]):
        if "cello" in inst_lower:
            return """
CELLO INSTRUMENT GUIDELINES:
- Focus on rich, warm melodic lines in mid-low register
- Create flowing legato passages with occasional pizzicato
- Use string-crossing patterns and position changes
- Velocity range 50-115 for expressive bowing dynamics
"""
        elif "violin" in inst_lower:
            return """
VIOLIN INSTRUMENT GUIDELINES:
- Create soaring melodic lines with expressive phrasing
- Include techniques like slurs, vibrato-friendly sustained notes
- Use string crossings and position changes naturally
- Velocity range 45-120 for expressive bow dynamics
"""
        else:
            return """
STRING INSTRUMENT GUIDELINES:
- Create flowing, lyrical melodic lines
- Use natural string instrument ranges and techniques
- Focus on legato phrasing with occasional articulated passages
- Build expressive crescendos and diminuendos through velocity
- Velocity range 45-115 for realistic string dynamics
"""
    
    # Brass instruments guidance
    elif any(word in inst_lower for word in ["trumpet", "trombone", "horn", "brass", "tuba"]):
        if "tuba" in inst_lower:
            return """
TUBA INSTRUMENT GUIDELINES:
- Create strong bass foundation with rhythmic emphasis
- Use sustained notes and rhythmic punctuation
- Focus on fundamental harmony and bass line movement
- Velocity range 80-120 for powerful brass presence
"""
        else:
            return """
BRASS INSTRUMENT GUIDELINES:
- Create bold, fanfare-like melodic lines
- Use brass-friendly keys and natural harmonics
- Include sustained notes and rhythmic articulation
- Build dramatic crescendos and accents
- Velocity range 70-127 for powerful brass dynamics
- Consider muted vs open brass timbres
"""
    
    # Woodwind instruments guidance
    elif any(word in inst_lower for word in ["flute", "clarinet", "sax", "oboe", "bassoon"]):
        return """
WOODWIND INSTRUMENT GUIDELINES:
- Create flowing, breath-aware melodic phrases
- Use natural scales and arpeggiated patterns
- Include breathing spaces between long phrases
- Focus on lyrical expression and smooth voice leading
- Velocity range 50-110 for realistic wind dynamics
- Consider the instrument's sweet spots and registers
"""
    
    # Synth instruments guidance
    elif any(word in inst_lower for word in ["synth", "lead", "pad", "electronic"]):
        return """
SYNTHESIZER INSTRUMENT GUIDELINES:
- Create modern, electronic-style patterns
- Use full range capabilities of synthesizers
- Include rhythmic sequences, arpeggios, or sustained pads
- Experiment with different velocity ranges for filter/envelope effects
- Velocity range 60-127 for full synthesizer expression
- Consider sequence-based or pattern-based compositions
"""
    
    # Drum guidance
    elif layer == "drums":
        return """
DRUM PATTERN GUIDELINES:
- Use standard GM drum mapping: Kick(36), Snare(38), Hi-hat(42), etc.
- Create rhythmic patterns with kick, snare, and hi-hat foundation
- Add percussion elements: crash(49), ride(51), toms(41,43,45,47,48,50)
- Velocity range 60-127 for dynamic drum hits
- Focus on groove and rhythmic interest
"""
    
    # Default guidance
    else:
        return """
GENERAL INSTRUMENT GUIDELINES:
- Use appropriate range and techniques for the specified instrument
- Create musically coherent patterns that suit the instrument's characteristics
- Focus on playability and realistic performance techniques
- Use velocity range 50-120 for natural expression
"""

    """Get genre-specific composition guidance."""
    
    genre_lower = genre.lower().replace("_", " ").replace("-", " ")
    
    if "rock" in genre_lower:
        return f"""
ROCK GENRE GUIDELINES:
- Use power chords, strong rhythmic patterns, and driving energy
- Focus on 4/4 time with emphasis on beats 1 and 3
- {layer} should have rock-appropriate dynamics and phrasing
- Include characteristic rock rhythms like eighth note drives or syncopation
- BPM {bpm} suggests {'mid-tempo rock' if 90 <= bpm <= 130 else 'fast rock energy' if bpm > 130 else 'ballad rock feel'}
"""
    
    elif "jazz" in genre_lower:
        return f"""
JAZZ GENRE GUIDELINES:
- Use sophisticated harmony, swing rhythms, and complex chord progressions
- Include syncopation, off-beat accents, and jazz-style phrasing
- {layer} should incorporate jazz scales, blue notes, and chromatic passing tones
- Focus on improvisation-friendly patterns and chord extensions
- BPM {bpm} suggests {'swing ballad' if bpm < 90 else 'medium swing' if bpm <= 140 else 'bebop tempo'}
"""
    
    elif "classical" in genre_lower:
        return f"""
CLASSICAL GENRE GUIDELINES:
- Use traditional classical harmony, counterpoint, and form principles
- Focus on melodic development, voice leading, and harmonic progression
- {layer} should follow classical composition techniques and phrasing
- Include proper voice leading and traditional classical rhythmic patterns
- BPM {bpm} suggests {'andante/moderate' if 76 <= bpm <= 108 else 'allegro/fast' if bpm > 108 else 'adagio/slow'}
"""
    
    elif "electronic" in genre_lower or "edm" in genre_lower:
        return f"""
ELECTRONIC/EDM GENRE GUIDELINES:
- Use repetitive patterns, build-ups, and electronic-style progressions
- Focus on rhythmic precision, sequence-based patterns, and electronic textures
- {layer} should incorporate electronic music elements like arpeggios or step sequences
- Include modern electronic rhythmic patterns and synthetic-friendly voicings
- BPM {bpm} suggests {'downtempo electronic' if bpm < 100 else 'house/techno' if 120 <= bpm <= 135 else 'drum & bass/hardcore' if bpm > 140 else 'electronic'}
"""
    
    elif "blues" in genre_lower:
        return f"""
BLUES GENRE GUIDELINES:
- Use 12-bar blues progression, blue notes, and traditional blues scales
- Focus on call-and-response patterns and blues-specific phrasing
- {layer} should incorporate blues scales, bends (velocity variations), and blues rhythm
- Include characteristic blues rhythms like shuffle or straight blues feel
- BPM {bpm} suggests {'slow blues' if bpm < 80 else 'medium blues' if bpm <= 120 else 'fast blues/boogie'}
"""
    
    elif "folk" in genre_lower or "acoustic" in genre_lower:
        return f"""
FOLK/ACOUSTIC GENRE GUIDELINES:
- Use simple, memorable melodies and traditional harmonic progressions
- Focus on singable melodies, open chords, and acoustic instrument techniques
- {layer} should be organic and natural-sounding with traditional phrasing
- Include folk-style strumming patterns or fingerpicking elements
- BPM {bpm} suggests {'ballad folk' if bpm < 90 else 'moderate folk' if bpm <= 120 else 'uptempo folk/country'}
"""
    
    elif "latin" in genre_lower or "salsa" in genre_lower or "bossa" in genre_lower:
        return f"""
LATIN GENRE GUIDELINES:
- Use Latin rhythms like clave, montuno, or bossa nova patterns
- Focus on syncopated rhythms, Latin percussion, and characteristic chord progressions
- {layer} should incorporate Latin-style phrasing and rhythmic complexity
- Include traditional Latin harmonic progressions and rhythmic patterns
- BPM {bpm} suggests {'bossa nova' if 100 <= bpm <= 130 else 'salsa/mambo' if 150 <= bpm <= 200 else 'Latin style'}
"""
    
    elif "country" in genre_lower:
        return f"""
COUNTRY GENRE GUIDELINES:
- Use simple chord progressions, storytelling melodies, and country-style phrasing
- Focus on traditional country instruments and playing techniques
- {layer} should incorporate country-style licks, bends, and rhythmic feel
- Include characteristic country rhythms and harmonic progressions
- BPM {bpm} suggests {'country ballad' if bpm < 90 else 'country shuffle' if 90 <= bpm <= 130 else 'country rock/honky-tonk'}
"""
    
    else:  # general/default
        return f"""
GENERAL MUSICAL GUIDELINES:
- Create musically coherent patterns that fit the specified style
- Focus on appropriate harmonic progressions and melodic development for the genre
- {layer} should be well-structured with clear musical phrasing
- Use rhythmic patterns and dynamics appropriate for the musical context
- BPM {bpm} creates a {'relaxed' if bpm < 90 else 'moderate' if bpm <= 130 else 'energetic'} feel
"""