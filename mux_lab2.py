
"""mux_lab2.py

Лабораторная 2: 4‑к‑1 мультиплексор
===================================

• Шаг по времени dt = 1 µs  
• Самый короткий импульс = 10 µs ⇒ базовый период 20 µs  
• Каждый следующий сигнал имеет в 2 раза больший период

Сигналы
-------
index: 0  1   2   3   4   5
name : X1 X2  X3  X4  a1  a2
period: 20  40  80  160  320  640  (µs)

Логические «1» = 5 В, «0» = 0 В.

Схема задержек
--------------
NOT  – 1 µs  
AND  – 1 µs  
OR   – 1 µs

Модель задержки: на каждом такте выход элемента вычисляется
из входов на предыдущем такте.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------- параметры моделирования ----------------
dt = 1e-6                    # шаг, 1 µs
t_base_pulse = 10e-6         # длительность «1» и «0» у самого быстрого меандра
logic_hi, logic_lo = 5.0, 0.0
num_lines = 6                # X1..X4,a1,a2
periods = [2*t_base_pulse*(2**i) for i in range(num_lines)]
t_stop = periods[-1]*2       # 2 полных цикла самого медленного сигнала
t = np.arange(0, t_stop, dt)
# ---------------------------------------------------------

def meander(t: np.ndarray, period: float) -> np.ndarray:
    """Прямоугольный сигнал 0/5 В с коэффициентом заполнения 50 %."""
    phase = (t % period) < (period/2)
    return np.where(phase, logic_hi, logic_lo)

# формирование входных сигналов
signals = [meander(t, p) for p in periods]
X1, X2, X3, X4, a1, a2 = signals  # распаковка

# ----------------- функция мультиплексора ----------------
def mux_no_delay(X1,X2,X3,X4,a1,a2):
    """Мультиплексор 4‑к‑1 без задержек (идеальный)."""
    # адресные биты: a1 = старший, a2 = младший
    sel0 = (a1==logic_lo) & (a2==logic_lo)
    sel1 = (a1==logic_lo) & (a2==logic_hi)
    sel2 = (a1==logic_hi) & (a2==logic_lo)
    sel3 = (a1==logic_hi) & (a2==logic_hi)
    F = (sel0 * X1 +
         sel1 * X2 +
         sel2 * X3 +
         sel3 * X4)
    return F

F_ideal = mux_no_delay(X1,X2,X3,X4,a1,a2)

# ----------- моделирование схемы с задержками ------------
def mux_with_delays(X1,X2,X3,X4,a1,a2):
    n = len(a1)
    # инициализация внутренних линий
    not_a1 = np.zeros(n)
    not_a2 = np.zeros(n)
    S1 = np.zeros(n)  # выход дешифратора
    S2 = np.zeros(n)
    S3 = np.zeros(n)
    S4 = np.zeros(n)
    Y1 = np.zeros(n)  # после «И» с входом Xi
    Y2 = np.zeros(n)
    Y3 = np.zeros(n)
    Y4 = np.zeros(n)
    F =  np.zeros(n)

    for i in range(1, n):
        # задержка NOT
        not_a1[i] = logic_hi if a1[i-1]==logic_lo else logic_lo
        not_a2[i] = logic_hi if a2[i-1]==logic_lo else logic_lo

        # задержка AND (дешифратор)
        S1[i] = logic_hi if (not_a1[i-1]==logic_hi and not_a2[i-1]==logic_hi) else logic_lo
        S2[i] = logic_hi if (not_a1[i-1]==logic_hi and a2[i-1]==logic_hi) else logic_lo
        S3[i] = logic_hi if (a1[i-1]==logic_hi and not_a2[i-1]==logic_hi) else logic_lo
        S4[i] = logic_hi if (a1[i-1]==logic_hi and a2[i-1]==logic_hi) else logic_lo

        # задержка AND (выборка данных Xi)
        Y1[i] = logic_hi if (S1[i-1]==logic_hi and X1[i-1]==logic_hi) else logic_lo
        Y2[i] = logic_hi if (S2[i-1]==logic_hi and X2[i-1]==logic_hi) else logic_lo
        Y3[i] = logic_hi if (S3[i-1]==logic_hi and X3[i-1]==logic_hi) else logic_lo
        Y4[i] = logic_hi if (S4[i-1]==logic_hi and X4[i-1]==logic_hi) else logic_lo

        # задержка OR
        F[i] = logic_hi if (Y1[i-1]==logic_hi or Y2[i-1]==logic_hi
                            or Y3[i-1]==logic_hi or Y4[i-1]==logic_hi) else logic_lo
    return F

F_delay = mux_with_delays(X1,X2,X3,X4,a1,a2)

# ------------------------- графики ------------------------
def plot_signals():
    t_us = t*1e6  # time axis в µs

    plt.figure(figsize=(11,8))
    names = ["X1","X2","X3","X4","a1","a2","F_ideal","F_delay"]
    sigs = signals + [F_ideal, F_delay]
    offset = 8.0  # вертикальный сдвиг для наглядности
    for idx, s in enumerate(sigs[::-1]):            # рисуем снизу вверх
        plt.plot(t_us, s + idx*offset, label=names[::-1][idx])
    plt.yticks([(i*offset) for i in range(len(sigs))],
               names[::-1])
    plt.xlabel("Время, µs")
    plt.title("Мультиплексор 4‑к‑1: входы, выход без задержек и выход с задержками")
    plt.grid(True, which="both", axis="x", linestyle=":")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_signals()
