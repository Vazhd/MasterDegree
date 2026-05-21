# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict


def plot_ecg_with_peaks(filtered_signal: np.ndarray,
                        r_peak_indices: np.ndarray,
                        fs: float = 250.0,
                        title: str = "ЭКГ - Результат анализа") -> None:
    
    time_axis = np.arange(len(filtered_signal)) / fs

    fig, axes = plt.subplots(2, 1, figsize=(14, 8), gridspec_kw={'height_ratios': [3, 1]})

    ax1 = axes[0]
    ax1.plot(time_axis, filtered_signal, color='#1a73e8', linewidth=0.7,
             label='Отфильтрованный ЭКГ')

    if len(r_peak_indices) > 0:
        ax1.scatter(r_peak_indices / fs,
                    filtered_signal[r_peak_indices],
                    color='red', s=60, zorder=5, marker='v',
                    label=f'R-пики ({len(r_peak_indices)} шт.)')

    ax1.set_xlabel('Время (сек)', fontsize=12)
    ax1.set_ylabel('Амплитуда (усл. ед.)', fontsize=12)
    ax1.set_title(title, fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)

    # --- Нижний график: RR-интервалы (тахограмма) ---
    ax2 = axes[1]
    if len(r_peak_indices) > 1:
        rr_ms = np.diff(r_peak_indices) / fs * 1000.0
        rr_time = r_peak_indices[1:] / fs
        ax2.plot(rr_time, rr_ms, color='#e8710a', linewidth=1.2, marker='o',
                 markersize=3, label='RR-интервалы')
        ax2.set_ylabel('RR (мс)', fontsize=12)
        ax2.set_xlabel('Время (сек)', fontsize=12)
        ax2.set_title('Тахограмма (RR-интервалы)', fontsize=12)
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
    else:
        ax2.text(0.5, 0.5, 'Недостаточно данных для тахограммы',
                 ha='center', va='center', fontsize=12, transform=ax2.transAxes)

    plt.tight_layout()
    plt.savefig('ecg_plot.png', dpi=150, bbox_inches='tight')
    print("  >> График сохранен: ecg_plot.png")
    plt.show()


def _interpret_stress(hrv: Dict) -> str:
    """Простая интерпретация уровня стресса по SDNN и RMSSD."""
    lines = []

    sdnn = hrv.get('sdnn_ms')
    rmssd = hrv.get('rmssd_ms')
    bpm = hrv.get('bpm')

    if sdnn is not None:
        if sdnn > 100:
            lines.append(f"  SDNN = {sdnn} мс -- Высокая вариабельность (норма, низкий стресс)")
        elif sdnn > 50:
            lines.append(f"  SDNN = {sdnn} мс -- Умеренная вариабельность")
        else:
            lines.append(f"  SDNN = {sdnn} мс -- Низкая вариабельность (повышенный стресс)")

    if rmssd is not None:
        if rmssd > 40:
            lines.append(f"  RMSSD = {rmssd} мс -- Хорошая парасимпатическая активность")
        elif rmssd > 20:
            lines.append(f"  RMSSD = {rmssd} мс -- Умеренная парасимпатическая активность")
        else:
            lines.append(f"  RMSSD = {rmssd} мс -- Сниженная парасимпатическая активность")

    if bpm is not None:
        if 60 <= bpm <= 100:
            lines.append(f"  BPM = {bpm} -- Нормальный пульс покоя")
        elif bpm < 60:
            lines.append(f"  BPM = {bpm} -- Брадикардия (пульс ниже нормы)")
        else:
            lines.append(f"  BPM = {bpm} -- Тахикардия (пульс выше нормы)")

    return "\n".join(lines) if lines else "  Недостаточно данных для интерпретации."


def generate_report(hrv_metrics: Dict,
                    output_path: str = "ecg_report.txt") -> str:
    """Генерирует текстовый отчёт с метриками HRV.

    Параметры
    ----------
    hrv_metrics : dict
        Словарь метрик из compute_hrv().
    output_path : str
        Путь для сохранения отчёта.

    Возвращает
    ----------
    str
        Текст отчёта.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = []
    report.append("=" * 60)
    report.append("       ОТЧЕТ ПО АНАЛИЗУ ЭЛЕКТРОКАРДИОГРАММЫ")
    report.append("=" * 60)
    report.append(f"  Дата анализа:       {now}")
    report.append(f"  Обнаружено R-пиков: {hrv_metrics.get('num_peaks', '-')}")
    report.append("")
    report.append("-" * 60)
    report.append("  МЕТРИКИ ВАРИАБЕЛЬНОСТИ СЕРДЕЧНОГО РИТМА (HRV)")
    report.append("-" * 60)
    report.append(f"  Средний RR-интервал:  {hrv_metrics.get('mean_rr_ms', '-')} мс")
    report.append(f"  Средний пульс (BPM):  {hrv_metrics.get('bpm', '-')} уд/мин")
    report.append(f"  SDNN:                 {hrv_metrics.get('sdnn_ms', '-')} мс")
    report.append(f"  RMSSD:                {hrv_metrics.get('rmssd_ms', '-')} мс")
    report.append(f"  pNN50:                {hrv_metrics.get('pnn50_pct', '-')} %")
    report.append("")
    report.append("-" * 60)
    report.append("  ИНТЕРПРЕТАЦИЯ")
    report.append("-" * 60)
    report.append(_interpret_stress(hrv_metrics))
    report.append("")
    report.append("=" * 60)
    report.append("  Примечание: данные показатели являются приблизительными")
    report.append("  и предназначены для исследовательских целей.")
    report.append("=" * 60)

    text = "\n".join(report)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"  >> Отчет сохранен: {output_path}")
    return text
