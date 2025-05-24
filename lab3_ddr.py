
"""lab3_ddr.py

Лабораторная 3 — передача данных SDR vs DDR
==========================================

• Шаг моделирования dt = 1 µs  
• Период синхросигнала T = 20 µs  
• Логический «0» = 0 В, «1» = 5 В

SDR (Single Data Rate)  — данные фиксируются по фронту (1 бит / T).  
DDR (Double Data Rate) — данные фиксируются по фронту **и** спаду (2 бита / T).

Числа для передачи (8 бит):
   0x7A = 01111010₂
   0xFF = 11111111₂
   0x0F = 00001111₂

Передаём **LSB‑первым** (бит 0 идёт первым) — при просмотре графика
справа‑налево легко получить привычную запись числа (требование задания).
"""


import numpy as np
import matplotlib.pyplot as plt

# ---------------- базовые константы ----------------
dt = 1e-6          # 1 µs
T  = 20e-6         # 20 µs
U0, U1 = 0.0, 5.0

# ---------------- генератор тактов -----------------
def clock_signal(num_periods: int):
    """Возвращает массив значений синхросигнала (0/5 В)."""
    t = np.arange(0, num_periods*T, dt)
    high = (t % T) < (T/2)          # 50 % duty cycle
    clk = np.where(high, U1, U0)
    return t, clk

# --------------- числа и их биты -------------------
numbers = {
    '7A': 0x7A,
    'FF': 0xFF,
    '0F': 0x0F,
}

def int_to_bits(value: int, width: int = 8):
    """LSB‑первый список битов указанной ширины."""
    return [(value >> i) & 1 for i in range(width)]

# ------------ формирование SDR/DDR -----------------
def sdr_wave(bits):
    """SDR‑передача: 1 бит на период T."""
    n = len(bits)
    t = np.arange(0, n*T, dt)
    wave = np.zeros_like(t)
    for i, b in enumerate(bits):
        idx = (t >= i*T) & (t < (i+1)*T)
        wave[idx] = U1 if b else U0
    return t, wave

def ddr_wave(bits):
    """DDR‑передача: 2 бита на период T (бит0 на фронт, бит1 на спад)."""
    pairs = [bits[i:i+2] for i in range(0, len(bits), 2)]
    n_periods = len(pairs)
    t = np.arange(0, n_periods*T, dt)
    wave = np.zeros_like(t)

    for p_idx, pair in enumerate(pairs):
        b_front = pair[0]
        b_fall  = pair[1] if len(pair) > 1 else 0
        # интервалы
        idx_front = (t >= p_idx*T) & (t < p_idx*T + T/2)
        idx_fall  = (t >= p_idx*T + T/2) & (t < (p_idx+1)*T)
        wave[idx_front] = U1 if b_front else U0
        wave[idx_fall]  = U1 if b_fall  else U0
    return t, wave

# --------------- построение графиков ---------------
def plot_all():
    fig, axs = plt.subplots(3, 3, figsize=(13, 8), sharex='col',
                            gridspec_kw={'hspace':0.35})
    for col, (name, num) in enumerate(numbers.items()):
        bits = int_to_bits(num, 8)

        # --- clock (общий для обоих режимов) ---
        t_clk, clk = clock_signal(len(bits))  # 8 периодов достаточно
        axs[0, col].step(t_clk*1e6, clk, where='post')
        axs[0, col].set_title(f"Синхро‑сигнал (T = 20 µs) — {name}h")
        axs[0, col].set_ylabel('Clk, В')
        axs[0, col].set_ylim(-0.5, 5.5)
        axs[0, col].grid(True, axis='x', linestyle=':')

        # --- SDR ---
        t_sdr, w_sdr = sdr_wave(bits)
        axs[1, col].step(t_sdr*1e6, w_sdr, where='post')
        axs[1, col].set_ylabel('SDR, В')
        axs[1, col].set_ylim(-0.5, 5.5)
        axs[1, col].grid(True, axis='x', linestyle=':')

        # --- DDR ---
        t_ddr, w_ddr = ddr_wave(bits)
        axs[2, col].step(t_ddr*1e6, w_ddr, where='post')
        axs[2, col].set_ylabel('DDR, В')
        axs[2, col].set_ylim(-0.5, 5.5)
        axs[2, col].grid(True, axis='x', linestyle=':')

        # x‑axis label только внизу
        axs[2, col].set_xlabel('Время, µs')

    plt.suptitle('Передача чисел 0x7A, 0xFF, 0x0F: SDR vs DDR', fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

# ----------- печать длительностей ------------------
def print_durations():
    for name, num in numbers.items():
        bits = int_to_bits(num, 8)
        t_sdr, _ = sdr_wave(bits)
        t_ddr, _ = ddr_wave(bits)
        print(f"{name}h: длительность SDR = {t_sdr[-1]*1e6 + dt*1e6:.0f} µs, ",
              f"DDR = {t_ddr[-1]*1e6 + dt*1e6:.0f} µs")

# ----------------------------------------------------
if __name__ == '__main__':
    plot_all()
    print()
    print_durations()
