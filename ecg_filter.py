import numpy as np
from scipy.signal import butter, sosfiltfilt, iirnotch, filtfilt


def bandpass_filter(signal: np.ndarray, fs: float = 250.0,
                    lowcut: float = 0.5, highcut: float = 40.0,
                    order: int = 4) -> np.ndarray:
    
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], btype='band', output='sos')
    return sosfiltfilt(sos, signal)


def notch_filter(signal: np.ndarray, fs: float = 250.0,
                 freq: float = 50.0, quality: float = 30.0) -> np.ndarray:
    b, a = iirnotch(freq, quality, fs)
    return filtfilt(b, a, signal)


def filter_ecg(raw_signal: np.ndarray, fs: float = 250.0) -> np.ndarray:
    
    step1 = notch_filter(raw_signal, fs=fs)

    filtered = bandpass_filter(step1, fs=fs)

    return filtered
