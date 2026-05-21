import sys
import numpy as np
import pandas as pd

from ecg_filter import filter_ecg
from ecg_rpeak_detector import detect_r_peaks
from ecg_hrv_analysis import compute_hrv
from ecg_report import plot_ecg_with_peaks, generate_report


def load_ecg_csv(filepath: str):
    
    df = pd.read_csv(filepath)

    raw_signal = df['ECG_Value'].values.astype(float)

    timestamps = df['Timestamp'].values.astype(float)
    dt = np.median(np.diff(timestamps))
    fs_estimated = 1.0 / dt

    return raw_signal, fs_estimated


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'my_first_ecg.csv'
    print(f"\n{'='*60}")
    print(f"  АНАЛИЗ ЭКГ - Пайплайн")
    print(f"{'='*60}")
    print(f"  Файл: {csv_path}")

    print("\n[1/4] Загрузка данных...")
    raw_signal, fs = load_ecg_csv(csv_path)
    duration = len(raw_signal) / fs
    print(f"  >> {len(raw_signal)} отсчетов, fs ~ {fs:.1f} Гц, "
          f"длительность ~ {duration:.1f} сек")

    print("\n[2/4] Цифровая фильтрация (Bandpass 0.5-40 Гц + Notch 50 Гц)...")
    filtered = filter_ecg(raw_signal, fs=fs)
    print(f"  >> Готово. Размах сигнала: {filtered.min():.1f} - {filtered.max():.1f}")

    print("\n[3/4] Детекция R-пиков (алгоритм Пан-Томпкинса)...")
    r_peaks = detect_r_peaks(filtered, fs=fs)
    print(f"  >> Найдено {len(r_peaks)} R-пиков")

    print("\n[4/4] Расчёт метрик HRV...")
    hrv = compute_hrv(r_peaks, fs=fs)
    print(f"  >> BPM    = {hrv['bpm']}")
    print(f"  >> SDNN   = {hrv['sdnn_ms']} мс")
    print(f"  >> RMSSD  = {hrv['rmssd_ms']} мс")
    print(f"  >> pNN50  = {hrv['pnn50_pct']} %")

    print("\nГенерация отчёта...")
    report_text = generate_report(hrv)
    print("\n" + report_text)

    print("\nПостроение графика...")
    plot_ecg_with_peaks(filtered, r_peaks, fs=fs)

    print("\n[OK] Анализ завершен!\n")


if __name__ == '__main__':
    main()
