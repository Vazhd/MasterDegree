import numpy as np
from typing import Dict, Optional


def compute_hrv(r_peak_indices: np.ndarray,
                fs: float = 250.0) -> Dict[str, Optional[float]]:
    
    result: Dict[str, Optional[float]] = {
        'bpm': None,
        'sdnn_ms': None,
        'rmssd_ms': None,
        'pnn50_pct': None,
        'mean_rr_ms': None,
        'num_peaks': len(r_peak_indices),
        'rr_intervals_ms': None,
    }

    if len(r_peak_indices) < 2:
        return result

    rr_samples = np.diff(r_peak_indices)
    rr_ms = (rr_samples / fs) * 1000.0  # мс

    result['rr_intervals_ms'] = rr_ms

    mean_rr = np.mean(rr_ms)
    result['mean_rr_ms'] = round(float(mean_rr), 2)
    result['bpm'] = round(60000.0 / mean_rr, 1)

    result['sdnn_ms'] = round(float(np.std(rr_ms, ddof=1)), 2)

    diff_rr = np.diff(rr_ms)
    rmssd = np.sqrt(np.mean(diff_rr ** 2))
    result['rmssd_ms'] = round(float(rmssd), 2)

    nn50 = np.sum(np.abs(diff_rr) > 50.0)
    pnn50 = (nn50 / len(diff_rr)) * 100.0
    result['pnn50_pct'] = round(float(pnn50), 2)

    return result
