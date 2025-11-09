import os
from pathlib import Path
import pretty_midi
import soundfile as sf
import numpy as np
import fluidsynth
from typing import Optional

class AudioRenderer:
    """Renders MIDI files to WAV using FluidR3 soundfont."""
    
    def __init__(self, sample_rate: int = 44100, force_fluidsynth_drums: bool = False):
        self.sample_rate = sample_rate
        self.force_fluidsynth_drums = force_fluidsynth_drums
        # Use the FluidR3 soundfont
        self.soundfont_path = "soundfonts/FluidR3_GM/FluidR3_GM.sf2"
        
    def render_midi_to_wav(self, midi_path: Path, output_path: Path, layer_type: str = "melody", instrument_program: int = 0) -> bool:
        """Render a MIDI file to WAV audio using FluidSynth with FluidR3."""
        try:
            # Try FluidSynth with soundfont first, fall back to pretty_midi if needed
            if Path(self.soundfont_path).exists():
                # Always try FluidSynth first, but with better drum handling
                audio = self._render_with_fluidsynth(midi_path, layer_type, instrument_program)
            else:
                print("⚠️  FluidR3 soundfont not found, using basic synthesis")
                audio = self._render_with_pretty_midi(midi_path, layer_type)
            
            # Save as WAV
            sf.write(str(output_path), audio, self.sample_rate)
            return True
            
        except Exception as e:
            print(f"❌ Error rendering audio: {e}")
            return False
    
    def _render_with_fluidsynth(self, midi_path: Path, layer_type: str, instrument_program: int = 0) -> np.ndarray:
        """Render using FluidSynth with FluidR3 soundfont."""
        try:
            # Initialize FluidSynth
            fs = fluidsynth.Synth(samplerate=self.sample_rate)
            
            # Load the FluidR3 soundfont
            sfid = fs.sfload(self.soundfont_path)
            if sfid == -1:
                raise Exception("Failed to load FluidR3 soundfont")
            
            # Load and process the MIDI file
            midi_data = pretty_midi.PrettyMIDI(str(midi_path))
            
            # Set up channels and programs based on layer type
            self._setup_fluidsynth_instruments(fs, sfid, layer_type, instrument_program)
            
            # Calculate duration and prepare audio buffer
            duration = max(4.0, midi_data.get_end_time())  # Minimum 4 seconds
            total_samples = int(duration * self.sample_rate)
            
            # Process all MIDI events
            events = []
            for instrument in midi_data.instruments:
                if layer_type == "drums":
                    # Force drums to channel 9 (0-indexed = 9)
                    channel = 9
                    instrument.is_drum = True
                else:
                    channel = 0  # Use channel 0 for melodic instruments
                
                for note in instrument.notes:
                    # Note on event
                    events.append((note.start, 'note_on', channel, note.pitch, note.velocity))
                    # Note off event  
                    events.append((note.end, 'note_off', channel, note.pitch, 64))
            
            # Sort events by time
            events.sort(key=lambda x: x[0])
            
            # Render audio
            audio_data = []
            current_time = 0.0
            
            for event_time, event_type, channel, pitch, velocity in events:
                # Render silence until next event
                if event_time > current_time:
                    silence_samples = int((event_time - current_time) * self.sample_rate)
                    if silence_samples > 0:
                        silence = fs.get_samples(silence_samples)
                        audio_data.extend(silence)
                
                # Send MIDI event
                if event_type == 'note_on':
                    fs.noteon(channel, pitch, velocity)
                elif event_type == 'note_off':
                    fs.noteoff(channel, pitch)
                    
                current_time = event_time
            
            # Render any remaining audio
            remaining_samples = total_samples - len(audio_data)
            if remaining_samples > 0:
                final_audio = fs.get_samples(remaining_samples)
                audio_data.extend(final_audio)
            
            # Convert to numpy array and normalize
            audio = np.array(audio_data, dtype=np.float32)
            if len(audio) > 0:
                max_val = np.max(np.abs(audio))
                if max_val > 0:
                    audio = audio / max_val * 0.8  # Normalize with headroom
            
            # Clean up FluidSynth
            fs.delete()
            
            return audio
            
        except Exception as e:
            print(f"⚠️  FluidSynth rendering failed ({e}), falling back to basic synthesis")
            return self._render_with_pretty_midi(midi_path, layer_type)
    
    def _setup_fluidsynth_instruments(self, fs: fluidsynth.Synth, sfid: int, layer_type: str, instrument_program: int = 0):
        """Set up FluidSynth instruments based on layer type."""
        if layer_type == "drums":
            # Set up drum kit on channel 9 (MIDI standard)
            # For FluidSynth, drum sounds are in bank 128, program 0
            fs.program_select(9, sfid, 128, 0)  # Channel 9, soundfont, bank 128, program 0
            print(f"🥁 FluidSynth: Set up drums on channel 9, bank 128, program 0")
        else:
            # Set up custom instrument on channel 0, bank 0
            fs.program_select(0, sfid, 0, instrument_program)
            print(f"🎵 FluidSynth: Set up {layer_type} on channel 0, bank 0, program {instrument_program}")
    
    def _render_with_pretty_midi(self, midi_path: Path, layer_type: str) -> np.ndarray:
        """Fallback: render using pretty_midi's built-in synthesizer."""
        try:
            midi_data = pretty_midi.PrettyMIDI(str(midi_path))
            
            # Set appropriate instruments
            self._set_instruments_for_layer(midi_data, layer_type)
            
            # For drums, ensure the instrument is properly marked as drums
            if layer_type == "drums":
                for instrument in midi_data.instruments:
                    instrument.is_drum = True
                    instrument.program = 0  # Standard kit
                    print(f"🥁 Drum instrument setup: is_drum={instrument.is_drum}, notes_count={len(instrument.notes)}")
            
            # Synthesize
            audio = midi_data.synthesize(fs=self.sample_rate)
            
            # Check if we got any audio
            if len(audio) == 0:
                print("⚠️  No audio generated, creating test tone")
                # Generate a simple test tone for debugging
                duration = 2.0  # 2 seconds
                t = np.linspace(0, duration, int(duration * self.sample_rate))
                audio = 0.3 * np.sin(2 * np.pi * 440 * t)  # 440Hz tone
            
            # Normalize
            if len(audio) > 0:
                max_val = np.max(np.abs(audio))
                if max_val > 0:
                    audio = audio / max_val * 0.8
                else:
                    print("⚠️  Audio is all zeros")
                    
            return audio
            
        except Exception as e:
            print(f"❌ Pretty_midi synthesis failed: {e}")
            # Return silence if all else fails
            return np.zeros(int(4.0 * self.sample_rate))
    
    def _set_instruments_for_layer(self, midi_data: pretty_midi.PrettyMIDI, layer_type: str):
        """Set appropriate instrument programs for different layer types."""
        instrument_map = {
            "melody": 0,     # Acoustic Grand Piano
            "bass": 32,      # Acoustic Bass
            "chords": 0,     # Acoustic Grand Piano
            "drums": 128,    # Drum kit
        }
        
        program = instrument_map.get(layer_type, 0)
        
        for instrument in midi_data.instruments:
            if layer_type == "drums":
                instrument.is_drum = True
                instrument.program = 0  # Drum programs start at 0 for drum channel
            else:
                instrument.program = program
                instrument.is_drum = False

def render_audio(midi_path: Path, output_dir: Path, layer_type: str, instrument_program: int = 0) -> Optional[Path]:
    """Convenience function to render MIDI to audio using FluidR3."""
    renderer = AudioRenderer()
    wav_path = output_dir / f"{layer_type}.wav"
    
    print(f"🎵 Rendering {layer_type} MIDI to audio with FluidR3...")
    
    if renderer.render_midi_to_wav(midi_path, wav_path, layer_type, instrument_program):
        print(f"✅ Audio saved to {wav_path}")
        return wav_path
    else:
        print(f"❌ Failed to render audio for {layer_type}")
        return None