import numpy as np


def sine_osc(
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


def square_osc(
        frequency: int = 440,
        duration: float = 1.0,
        amplitude: float = 0.5,
        sample_rate: int = 44100
) -> np.ndarray:
    """Generate a square tone"""

    # Calculate the number of samples needed
    n_samples = int(duration * sample_rate)

    # Create an array of time points
    time_points = np.linspace(0, duration, n_samples, False)

    # Create the sine wave
    sine = np.sin(2 * np.pi * frequency * time_points)

    # Create the square wave
    square = np.clip(sine * 10, -1, 1)

    # Scale by amplitude
    square *= amplitude

    return square


def triangular_osc(
        frequency: int = 440,
        duration: float = 1.0,
        amplitude: float = 0.5,
        sample_rate: int = 44100
) -> np.ndarray:
    """Generate a triangular tone"""

    # Calculate the number of samples needed
    n_samples = int(duration * sample_rate)

    # Create an array of time points
    time_points = np.linspace(0, duration, n_samples, False)

    # Create the sine wave
    sine = np.sin(2 * np.pi * frequency * time_points)

    # Create the square wave
    triangular = np.cumsum(np.clip(sine * 10, -1, 1))

    # Normalization
    triangular = triangular / np.max(triangular)

    # Scale by amplitude
    triangular *= amplitude

    return triangular
