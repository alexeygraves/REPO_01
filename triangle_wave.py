
"""triangle_wave.py

Визуализирует треугольные сигналы частотой 10 кГц, 5 кГц и 2 кГц (амплитуда 5 В)
и выход логического каскада со шмиттовским гистерезисом 2…4 В.
"""

import numpy as np
import matplotlib.pyplot as plt


# --- параметры задачи ---
AMP = 5.0                        # амплитуда треугольника, В
FREQ_LIST = [10e3, 5e3, 2e3]     # частоты, Гц
T_END = 1e-3                     # длительность визуализации, 1 мс
DT = 1e-6                        # шаг моделирования, 1 мкс
LOW_THR, HIGH_THR = 2.0, 4.0     # запрещённая зона
# -------------------------

t = np.arange(0, T_END, DT)      # временная сетка


def triangle_wave(t: np.ndarray, f: float, a: float) -> np.ndarray:
    """Генерирует треугольник 0…a (период 1/f)"""
    phase = (t * f) % 1.0        # дробная часть периода
    return np.where(phase < 0.5, 2 * a * phase, 2 * a * (1 - phase))


def schmitt_trigger(x: np.ndarray, low: float, high: float) -> np.ndarray:
    """0/5‑вольтовый выход с гистерезисом (low <-> high)."""
    out = np.zeros_like(x)
    state = 0.0
    for i, v in enumerate(x):
        if state == 0 and v > high:
            state = 5.0
        elif state == 5 and v < low:
            state = 0.0
        out[i] = state
    return out


def main() -> None:
    for f in FREQ_LIST:
        x = triangle_wave(t, f, AMP)
        y = schmitt_trigger(x, LOW_THR, HIGH_THR)

        plt.figure(figsize=(10, 4))
        plt.plot(t * 1e3, x, label=f"Вход: {f/1e3:.0f} кГц")
        plt.plot(t * 1e3, y, label="Выход каскада", linestyle="--")
        plt.hlines([LOW_THR, HIGH_THR], 0, T_END * 1e3,
                   linestyles="dotted", label="Запрещённая зона 2–4 В")
        plt.title(f"Треугольный сигнал {f/1e3:.0f} кГц и выход каскада")
        plt.xlabel("Время, мс")
        plt.ylabel("Напряжение, В")
        plt.ylim(-0.5, 5.5)
        plt.legend(loc="upper right")
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
