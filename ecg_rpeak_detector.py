# -*- coding: utf-8 -*-

import numpy as np


def _differentiate(signal: np.ndarray) -> np.ndarray:
    diff = np.zeros_like(signal)
    # y[n] = (1/8) * (-x[n-2] - 2x[n-1] + 2x[n+1] + x[n+2])
    for i in range(2, len(signal) - 2):
        diff[i] = (-signal[i - 2] - 2 * signal[i - 1]
                    + 2 * signal[i + 1] + signal[i + 2]) / 8.0
    return diff


def _squaring(signal: np.ndarray) -> np.ndarray:
    return signal ** 2


def _moving_average(signal: np.ndarray, window_size: int) -> np.ndarray:
    ma = np.convolve(signal, np.ones(window_size) / window_size, mode='same')
    return ma


def detect_r_peaks(filtered_signal: np.ndarray,
                   fs: float = 250.0) -> np.ndarray:
    
    diff = _differentiate(filtered_signal)

    squared = _squaring(diff)

    window_size = int(0.150 * fs)
    if window_size < 1:
        window_size = 1
    integrated = _moving_average(squared, window_size)

    learning_samples = int(2.0 * fs)
    learning_segment = integrated[:learning_samples]

    spki = np.max(learning_segment) * 0.25   
    npki = np.mean(learning_segment) * 0.5   
    threshold = npki + 0.25 * (spki - npki)

    refractory = int(0.200 * fs)

    r_peaks = []
    last_peak_idx = -refractory  

    for i in range(1, len(integrated) - 1):
        if (integrated[i] > integrated[i - 1] and
                integrated[i] >= integrated[i + 1]):

            if integrated[i] > threshold:
                if (i - last_peak_idx) > refractory:
                    
                    search_half = int(0.075 * fs)
                    lo = max(0, i - search_half)
                    hi = min(len(filtered_signal), i + search_half)
                    refined = lo + np.argmax(filtered_signal[lo:hi])

                    r_peaks.append(refined)
                    last_peak_idx = i

                    spki = 0.125 * integrated[i] + 0.875 * spki
                else:
                    npki = 0.125 * integrated[i] + 0.875 * npki
            else:
                npki = 0.125 * integrated[i] + 0.875 * npki

            threshold = npki + 0.25 * (spki - npki)

    return np.array(r_peaks, dtype=int)
