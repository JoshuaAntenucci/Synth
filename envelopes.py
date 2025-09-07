import numpy as np


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

    return sound
