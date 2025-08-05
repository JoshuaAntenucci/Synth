import numpy as np
import sounddevice as sd
from pynput.keyboard import Listener, Key


def main():
    def press_on(key):
        print("Press ON: {}".format(key))

        if hasattr(key, 'char') and key.char == 'a':
            play_sound()

    def press_off(key):
        print("Press OFF: {}".format(key))
        sd.stop()

        if key == Key.esc:
            return False

    with Listener(on_press=press_on, on_release=press_off) as listener:  # type: ignore
        listener.join()


def play_sound():
    # Generate and play a sound
    # sine1 = sine_tone(200, 1, 0.6)
    # sine2 = sine_tone(400, 1, 0.3)
    # sine3 = sine_tone(800, 1, 0.2)

    # Generate mupltiple sine waves with varying frequencies and amplitudes
    # sines = [sine_tone(frequency=200 * i, amplitude=0.7 / i)
    #          for i in range(1, 31, 2)]

    # mysound = sum(sines)
    # mysound = sum([sine1, sine2, sine3])

    # my_sound = sine_tone(frequency=300, duration=0.3)
    # my_sound = apply_envelope(my_sound, [0.5, 0.2, 0.6, 0.5])
    # my_sound = apply_envelope(my_sound, [0.02, 0.1, 0.3, 0.1])
    # my_sound = apply_envelope(my_sound, [1.0, 0.5, 0.7, 1.0])

    # Create a modulator wave
    my_modulator = sine_tone(3, 3)

    # Apply amplitude modulation
    # am_sound = am_synthesis(220, my_modulator)
    # am_sound = am_synthesis(230, am_sound)

    # Apply frequency modulation
    # fm_sound = fm_synthesis(220, my_modulator)

    # Apply modulation
    modulated_sound = am_synthesis(2, my_modulator)
    modulated_sound = am_synthesis(440, modulated_sound)
    modulated_sound = fm_synthesis(217, modulated_sound, modulation_index=5)
    modulated_sound = fm_synthesis(2, modulated_sound)
    modulated_sound = am_synthesis(110, modulated_sound)
    modulated_sound = fm_synthesis(220, modulated_sound, modulation_index=5)

    modulated_sound = apply_envelope(modulated_sound, [1.0, 0.5, 0.7, 1.0])

    sd.play(modulated_sound)
    sd.wait()


def sine_tone(
        frequency: int = 440,
        duration: float = 1.0,
        amplitude: float = 0.5,
        sample_rate: int = 44100
) -> np.ndarray:
    """Generate a sine tone"""

    # Calculate the number of samples needed
    n_samples = int(duration * sample_rate)

    # Create an array of time points
    time_points = np.linspace(0, duration, n_samples, False)

    # Create the sine wave
    sine = np.sin(2 * np.pi * frequency * time_points)

    # Scale by amplitude
    sine *= amplitude

    return sine


def white_noise(duration: float = 1.0, amplitude: float = 0.5, sample_rate: int = 44100) -> np.ndarray:
    """Generate white noise"""

    # Calculate the number of samples needed
    n_samples = int(duration * sample_rate)

    # Generate white noise with values between -1 and 1
    noise = np.random.uniform(-1, 1, n_samples)

    # Scale by amplitude
    noise *= amplitude

    return noise


def apply_envelope(sound: np.ndarray, adsr: list, sample_rate: int = 44100) -> np.ndarray:
    """Apply an ADSR envelope
    A, D, R in time in seconds
    S in % volume
    """

    # Copy sound to prevent modifyng the original
    sound = sound.copy()

    # Calculate the number of samples for each stage
    attack_samples = int(adsr[0] * sample_rate)
    decay_samples = int(adsr[1] * sample_rate)
    release_samples = int(adsr[3] * sample_rate)
    sustain_samples = len(sound) - (attack_samples +
                                    decay_samples + release_samples)

    # Attack
    sound[:attack_samples] *= np.linspace(0, 1, attack_samples)

    # Decay
    sound[attack_samples:attack_samples +
          decay_samples] *= np.linspace(1, adsr[2], decay_samples)

    # Sustain
    sound[attack_samples + decay_samples:attack_samples +
          decay_samples + sustain_samples] *= adsr[2]

    # Release
    sound[attack_samples + decay_samples +
          sustain_samples:] *= np.linspace(adsr[2], 0, release_samples)

    # print(attack_samples, decay_samples, release_samples, sustain_samples)

    return sound


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


main()
