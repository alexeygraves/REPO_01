
"""priority_encoder.py

Приоритетный шифратор 4→2 с выходом EO
======================================

X1 – самый высокий приоритет, X4 – самый низкий.

Выходы:
    a1 a2 – двоичный номер активного устройства
             (X1 = 0, X2 = 1, X3 = 2, X4 = 3)
    EO     – 1, если НИ ОДНО устройство не активно

Моделирование
-------------
• шаг dt = 1 µs
• Формируем меандры, где каждый следующий сигнал имеет
  в 2 раза больший период → за 16 тактов проходят все 16
  комбинаций входов (0000 … 1111).
"""

import numpy as np
import matplotlib.pyplot as plt

# -------- параметры моделирования -------------
dt = 1e-6
t_steps = 16            # 16 комбинаций
t = np.arange(0, t_steps*dt, dt)

logic_lo, logic_hi = 0.0, 5.0


def meander(t, base_period, index):
    """Сигнал с периодом base_period*2**index и скважностью 50 %."""
    period = base_period * (2 ** index)
    return np.where((t % period) < (period / 2), logic_hi, logic_lo)


# формируем 4 входных сигнала
base_period = 2 * dt
X = [meander(t, base_period, i) for i in range(4)]
X1, X2, X3, X4 = X

# ----- логика приоритетного шифратора 4→2 -----
def priority_encoder(x1, x2, x3, x4):
    """Возвращает a1, a2, EO для массивов входов."""
    n = len(x1)
    a1 = np.zeros(n)
    a2 = np.zeros(n)
    eo = np.zeros(n)

    for i in range(n):
        if x1[i] == logic_hi:          # устройство 0
            a1[i], a2[i] = logic_lo, logic_lo
        elif x2[i] == logic_hi:        # устройство 1
            a1[i], a2[i] = logic_lo, logic_hi
        elif x3[i] == logic_hi:        # устройство 2
            a1[i], a2[i] = logic_hi, logic_lo
        elif x4[i] == logic_hi:        # устройство 3
            a1[i], a2[i] = logic_hi, logic_hi
        else:                          # ни одного запроса
            eo[i] = logic_hi
            a1[i], a2[i] = logic_lo, logic_lo
    return a1, a2, eo


a1, a2, eo = priority_encoder(X1, X2, X3, X4)

# ----------------- график ---------------------
def plot_all():
    names = ["X1", "X2", "X3", "X4", "a1", "a2", "EO"]
    sigs = [X1, X2, X3, X4, a1, a2, eo]
    offset = 6.0
    t_us = t * 1e6

    plt.figure(figsize=(11, 6))
    for idx, s in enumerate(sigs[::-1]):
        plt.step(t_us, s + idx*offset, where="post", label=names[::-1][idx])
    plt.yticks([(i*offset) for i in range(len(sigs))], names[::-1])
    plt.xlabel("Время, µs")
    plt.title("Приоритетный шифратор 4→2: входы и выходы")
    plt.grid(True, axis="x", linestyle=":")
    plt.tight_layout()
    plt.show()


def print_truth_table():
    print("Таблица истинности приоритетного шифратора 4→2 (X1‑X4):\n")
    print("X1 X2 X3 X4 | a1 a2 | EO")
    print("-"*26)
    for X1b in (0,1):
        for X2b in (0,1):
            for X3b in (0,1):
                for X4b in (0,1):
                    a1b, a2b, eob = priority_encoder(
                        np.array([logic_hi if X1b else logic_lo]),
                        np.array([logic_hi if X2b else logic_lo]),
                        np.array([logic_hi if X3b else logic_lo]),
                        np.array([logic_hi if X4b else logic_lo])
                    )
                    print(f" {X1b}  {X2b}  {X3b}  {X4b} |  {int(a1b[0])}  {int(a2b[0])} | {int(eob[0])}")
    print("\nПриоритет: X1 > X2 > X3 > X4")


if __name__ == "__main__":
    print_truth_table()
    plot_all()
