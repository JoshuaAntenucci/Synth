import numpy as np


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
