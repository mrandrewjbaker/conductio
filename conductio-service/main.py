import argparse
import sys
from generation.layer_runner import run_layer
from generation.wizard import run_wizard

if __name__ == "__main__":
    # Check if running in wizard mode
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in ["--wizard", "-w"]):
        run_wizard()
        sys.exit(0)
    
    parser = argparse.ArgumentParser(description="Conductio-AI Layer Generator")
    parser.add_argument("--layer", help="melody | drums | bass | chords")
    parser.add_argument("--key", default="C minor")
    parser.add_argument("--bpm", type=int, default=120)
    parser.add_argument("--bars", type=int, default=8)
    parser.add_argument("--instrument", default="auto", help="GM instrument name or number (e.g., 'electric_guitar', 'violin', '25')")
    parser.add_argument("--genre", default="general", help="Musical genre (rock, jazz, classical, electronic, blues, folk, latin, country)")
    parser.add_argument("--no-audio", action="store_true", help="Skip audio rendering (MIDI only)")
    parser.add_argument("--wizard", "-w", action="store_true", help="Run interactive wizard")
    parser.add_argument("--list-instruments", action="store_true", help="List all available instruments")
    args = parser.parse_args()
    
    if args.wizard:
        run_wizard()
        sys.exit(0)
    
    if args.list_instruments:
        from generation.instruments import list_instruments_by_category
        print("🎼 Available Instruments by Category:")
        print("=" * 50)
        
        categories = list_instruments_by_category()
        for category, instruments in categories.items():
            print(f"\n🎵 {category}:")
            for name, program in instruments:
                display_name = name.replace("_", " ").title()
                print(f"   {program:3d}. {display_name} ({name})")
        
        print(f"\n💡 Total: {len(sum(categories.values(), []))} instruments")
        print("💡 Use instrument names in lowercase with underscores (e.g., 'electric_guitar')")
        sys.exit(0)
    
    if not args.layer:
        print("❌ Error: --layer is required when not using wizard mode")
        print("💡 Try: python main.py --wizard")
        sys.exit(1)
    
    render_audio = not args.no_audio
    run_layer(layer=args.layer, key=args.key, bpm=args.bpm, bars=args.bars, 
              instrument=args.instrument, render_audio_flag=render_audio, genre=args.genre)