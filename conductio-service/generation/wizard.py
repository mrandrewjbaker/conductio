import os
from typing import Dict, List, Tuple
from generation.layer_runner import run_layer
from generation.instruments import list_instruments_by_category, get_instrument_program

def run_wizard():
    """Interactive wizard for Conductio music generation."""
    print("🎵 Welcome to the Conductio Music Generation Wizard! 🎵")
    print("=" * 60)
    
    try:
        # Get layer type
        layer = get_layer_choice()
        
        # Get genre
        genre = get_genre_choice()
        
        # Get musical parameters
        key = get_key_choice()
        bpm = get_bpm_choice()
        bars = get_bars_choice()
        
        # Get instrument (skip for drums)
        if layer != "drums":
            instrument = get_instrument_choice(layer)
        else:
            instrument = "auto"  # Drums always use drum kit
        
        # Get audio rendering preference
        render_audio = get_audio_choice()
        
        # Show summary and confirm
        show_generation_summary(layer, genre, key, bpm, bars, instrument, render_audio)
        
        if confirm_generation():
            print("\n🚀 Starting generation...")
            run_layer(layer=layer, key=key, bpm=bpm, bars=bars, 
                     instrument=instrument, render_audio_flag=render_audio, genre=genre)
        else:
            print("❌ Generation cancelled.")
            
    except KeyboardInterrupt:
        print("\n\n❌ Wizard cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error in wizard: {e}")

def get_layer_choice() -> str:
    """Get layer type from user."""
    print("\n1️⃣ Choose Layer Type:")
    print("   🎹 melody  - Lead melodic lines, hooks, themes")
    print("   🎸 bass    - Low-frequency foundation, root notes")
    print("   🥁 drums   - Rhythmic percussion patterns")
    print("   🎼 chords  - Harmonic progressions, accompaniment")
    
    while True:
        choice = input("\nEnter layer type (melody/bass/drums/chords): ").strip().lower()
        if choice in ["melody", "bass", "drums", "chords"]:
            return choice
        print("❌ Invalid choice. Please enter: melody, bass, drums, or chords")

def get_genre_choice() -> str:
    """Get musical genre from user with open-ended input."""
    print("\n2️⃣ Choose Musical Genre:")
    print("   💡 Enter any genre or style you want (e.g., 'rock', 'jazz', 'electronic', 'classical')")
    print("   💡 You can be specific: 'bossa nova', 'death metal', 'ambient', 'country blues'")
    print("   💡 Or leave blank for general/neutral style")
    
    while True:
        choice = input("\nEnter genre (or press Enter for general): ").strip()
        if choice == "":
            return "general"
        elif len(choice) >= 2:  # Minimum reasonable genre length
            return choice
        print("❌ Please enter a genre name (at least 2 characters) or press Enter for general")

def get_key_choice() -> str:
    """Get musical key from user."""
    print("\n3️⃣ Choose Musical Key:")
    
    # Popular keys organized by mood
    keys = {
        "🌟 Popular Major": ["C major", "G major", "D major", "A major", "E major", "F major"],
        "🌙 Popular Minor": ["A minor", "E minor", "B minor", "D minor", "G minor", "F# minor"],
        "🎭 Character Keys": ["Bb major", "Eb major", "Ab major", "C# minor", "F minor", "Bb minor"]
    }
    
    for category, key_list in keys.items():
        print(f"\n   {category}:")
        for i, key in enumerate(key_list, 1):
            print(f"     {i}. {key}")
    
    print("\n   Or enter any key manually (e.g., 'F# major', 'Db minor')")
    
    while True:
        choice = input("\nEnter key: ").strip()
        if choice:
            return choice
        print("❌ Please enter a musical key")

def get_bpm_choice() -> int:
    """Get tempo from user."""
    print("\n4️⃣ Choose Tempo (BPM):")
    
    tempo_ranges = [
        ("🐌 Slow Ballad", "60-80 BPM", [60, 70, 80]),
        ("🚶 Medium", "90-120 BPM", [90, 100, 110, 120]),
        ("🏃 Upbeat", "130-150 BPM", [130, 140, 150]),
        ("🚀 Fast/Electronic", "160-180 BPM", [160, 170, 180])
    ]
    
    for category, desc, bpms in tempo_ranges:
        print(f"\n   {category} ({desc}):")
        for bpm in bpms:
            print(f"     {bpm}")
    
    while True:
        try:
            choice = input("\nEnter BPM (60-200): ").strip()
            bpm = int(choice)
            if 60 <= bpm <= 200:
                return bpm
            print("❌ BPM must be between 60 and 200")
        except ValueError:
            print("❌ Please enter a valid number")

def get_bars_choice() -> int:
    """Get number of bars from user."""
    print("\n5️⃣ Choose Length (Bars):")
    
    length_options = [
        ("🎵 Short Loop", "1-4 bars", [1, 2, 4]),
        ("🎶 Standard Phrase", "8-16 bars", [8, 12, 16]),
        ("🎼 Extended Section", "24-32 bars", [24, 28, 32])
    ]
    
    for category, desc, bars_list in length_options:
        print(f"\n   {category} ({desc}):")
        for bars in bars_list:
            print(f"     {bars}")
    
    while True:
        try:
            choice = input("\nEnter number of bars (1-64): ").strip()
            bars = int(choice)
            if 1 <= bars <= 64:
                return bars
            print("❌ Number of bars must be between 1 and 64")
        except ValueError:
            print("❌ Please enter a valid number")

def get_instrument_choice(layer: str) -> str:
    """Get instrument choice from user."""
    print(f"\n6️⃣ Choose Instrument for {layer.title()} Layer:")
    
    # Show popular instruments by category
    categories = list_instruments_by_category()
    
    # Show most relevant categories first based on layer
    if layer == "melody":
        priority_cats = ["Popular", "Piano", "Guitar", "Strings", "Brass", "Woodwinds", "Synth"]
    elif layer == "bass":
        priority_cats = ["Bass", "Popular", "Guitar", "Synth"]
    else:  # chords
        priority_cats = ["Piano", "Popular", "Guitar", "Strings", "Synth"]
    
    # Show categories in priority order
    for cat_name in priority_cats:
        if cat_name in categories:
            instruments = categories[cat_name]
            print(f"\n   🎵 {cat_name}:")
            
            # Format in columns (2 columns for better fit in wizard)
            formatted_instruments = []
            for name, program in instruments[:6]:  # Limit to 6 per category
                display_name = name.replace("_", " ").title()
                formatted_instruments.append(f"• {display_name}")
            
            # Display in 2 columns
            cols = 2
            col_width = 30
            for i in range(0, len(formatted_instruments), cols):
                row = formatted_instruments[i:i+cols]
                # Pad each column to consistent width
                padded_row = [f"{item:<{col_width}}" for item in row]
                print("     " + "".join(padded_row))
    
    print(f"\n   💡 Type 'list' to see all {len(sum(categories.values(), []))} available instruments")
    print("   💡 You can also enter GM program numbers (0-127)")
    print("   💡 Type 'auto' to use the default for this layer")
    
    while True:
        choice = input(f"\nEnter instrument name: ").strip().lower()
        
        if choice == "auto":
            return "auto"
        elif choice == "list":
            show_all_instruments()
            continue
        elif choice:
            try:
                # Try to resolve the instrument
                get_instrument_program(choice)
                return choice
            except ValueError as e:
                print(f"❌ {e}")
                continue
        else:
            print("❌ Please enter an instrument name or 'auto'")

def show_all_instruments():
    """Show all available instruments organized by category in column format."""
    print("\n" + "="*80)
    print("🎼 ALL AVAILABLE INSTRUMENTS")
    print("="*80)
    
    categories = list_instruments_by_category()
    
    for category, instruments in categories.items():
        if category == "Popular":  # Skip popular, already shown
            continue
        
        print(f"\n🎵 {category}:")
        print("-" * 78)
        
        # Format instruments in columns (3 columns)
        formatted_instruments = []
        for name, program in instruments:
            display_name = name.replace("_", " ").title()
            formatted_instruments.append(f"{program:3d}. {display_name}")
        
        # Display in 3 columns
        cols = 3
        col_width = 25
        for i in range(0, len(formatted_instruments), cols):
            row = formatted_instruments[i:i+cols]
            # Pad each column to consistent width
            padded_row = [f"{item:<{col_width}}" for item in row]
            print("  " + "".join(padded_row))
    
    print("\n" + "="*80)
    input("Press Enter to continue...")

def get_audio_choice() -> bool:
    """Get audio rendering preference from user."""
    print("\n7️⃣ Audio Rendering:")
    print("   🎵 yes - Generate both MIDI and high-quality WAV audio (recommended)")
    print("   📝 no  - Generate MIDI only (faster, for testing or DAW import)")
    
    while True:
        choice = input("\nGenerate audio? (yes/no) [yes]: ").strip().lower()
        if choice in ["", "y", "yes"]:
            return True
        elif choice in ["n", "no"]:
            return False
        print("❌ Please enter 'yes' or 'no'")

def show_generation_summary(layer: str, genre: str, key: str, bpm: int, bars: int, instrument: str, render_audio: bool):
    """Show summary of selected options."""
    print("\n" + "="*60)
    print("🎯 GENERATION SUMMARY")
    print("="*60)
    print(f"Layer:      {layer.title()}")
    print(f"Genre:      {genre.title()}")
    print(f"Key:        {key}")
    print(f"Tempo:      {bpm} BPM")
    print(f"Length:     {bars} bars")
    
    if instrument == "auto":
        print(f"Instrument: Auto (default for {layer})")
    else:
        try:
            program = get_instrument_program(instrument)
            print(f"Instrument: {instrument.replace('_', ' ').title()} (GM {program})")
        except:
            print(f"Instrument: {instrument}")
    
    print(f"Audio:      {'Yes (MIDI + WAV)' if render_audio else 'No (MIDI only)'}")
    print("="*60)

def confirm_generation() -> bool:
    """Ask user to confirm generation."""
    while True:
        choice = input("\n🚀 Generate music with these settings? (yes/no) [yes]: ").strip().lower()
        if choice in ["", "y", "yes"]:
            return True
        elif choice in ["n", "no"]:
            return False
        print("❌ Please enter 'yes' or 'no'")