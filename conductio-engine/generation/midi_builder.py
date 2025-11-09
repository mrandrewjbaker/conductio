from mido import MidiFile, MidiTrack, Message

def build_midi(pattern, output_path, layer_type="melody", instrument_program=0):
    """Convert pattern list into a basic single-track MIDI file."""
    mid = MidiFile(type=1, ticks_per_beat=480)
    track = MidiTrack()
    
    # Set appropriate channel for the layer type
    channel = 9 if layer_type == "drums" else 0
    
    # Add a program change (except for drums)
    if layer_type != "drums":
        track.append(Message("program_change", program=instrument_program, time=0, channel=channel))
    
    # Calculate timing for events
    for event in pattern:
        note_on = Message("note_on", note=event["note"], velocity=event["velocity"], time=0, channel=channel)
        note_off = Message("note_off", note=event["note"], velocity=64, time=event["duration"], channel=channel)
        
        track.append(note_on)
        track.append(note_off)
    
    mid.tracks.append(track)
    mid.save(output_path)