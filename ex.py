import numpy as np
import sounddevice as sd

# Configuration for the audio stream
samplerate = 44100  # samples per second
duration = 5.0      # seconds
channels = 1        # mono audio


def am_synthesis(
    carrier_frequency: float,
    modulator_wave: np.ndarray,
    modulation_index: float = 0.5,
    amplitude: float = 0.5,
    sample_rate: int = 44100
) -> np.ndarray:
    """Generates an AM synthesis waveform"""

    # Calculate the total number of samples needed
    total_samples = len(modulator_wave)

    # Create an array of time points
    time_points = np.arange(total_samples) / sample_rate

    # Generate the carrier wave
    carrier_wave = np.sin(2 * np.pi * carrier_frequency * time_points)

    # Apply the AM synthesis formula
    am_wave = (1 + modulation_index * modulator_wave) * carrier_wave

    # Normalize to an specified amplitude
    max_amplitude = np.max(np.abs(am_wave))
    am_wave = amplitude * (am_wave / max_amplitude)

    return am_wave


def fm_synthesis(
    carrier_frequency: float,
    modulator_wave: np.ndarray,
    modulation_index: float = 3,
    amplitude: float = 0.5,
    sample_rate: int = 44100
) -> np.ndarray:
    """Generate an FM synthesis waveform"""

    # Calculate the total number of samples needed
    total_samples = len(modulator_wave)

    # Create an array of time points
    time_points = np.arange(total_samples) / sample_rate

    # Create the FM signal
    fm_wave = np.sin(2 * np.pi * carrier_frequency *
                     time_points + modulation_index * modulator_wave)

    # Normalize to an specified amplitude
    max_amplitude = np.max(np.abs(fm_wave))
    fm_wave = amplitude * (fm_wave / max_amplitude)

    return fm_wave


# Generate sine wave data
frequency = 440  # Hz
t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)  # Amplitude 0.5

audio_data = am_synthesis(200, audio_data)

audio_data = am_synthesis(2, audio_data)
audio_data = am_synthesis(440, audio_data)
audio_data = fm_synthesis(217, audio_data, modulation_index=5)
audio_data = fm_synthesis(2, audio_data)
audio_data = am_synthesis(110, audio_data)
audio_data = fm_synthesis(220, audio_data, modulation_index=5)

# Initialize a variable to keep track of the current position in the audio data
current_frame = 0

# Define the callback function


def callback(outdata, frames, time, status):
    global current_frame
    if status:
        print(status)  # Print any status messages (e.g., underrun)

    # Calculate the number of frames to write from the remaining audio data
    remaining_frames = len(audio_data) - current_frame
    frames_to_write = min(frames, remaining_frames)

    # Write audio data to the output buffer
    outdata[:frames_to_write] = audio_data[current_frame: current_frame +
                                           frames_to_write].reshape(-1, channels)

    # Fill the rest of the buffer with zeros if less data is available
    if frames_to_write < frames:
        outdata[frames_to_write:] = 0.0
        raise sd.CallbackStop  # Stop the stream when data runs out

    current_frame += frames_to_write


# Create and start the OutputStream
try:
    with sd.OutputStream(samplerate=samplerate, channels=channels, callback=callback) as stream:
        print(f"Playing sine wave for {duration} seconds...")
        # Sleep slightly longer than duration to ensure playback finishes
        sd.sleep(int(duration * 1000) + 100)
except Exception as e:
    print(f"An error occurred: {e}")
