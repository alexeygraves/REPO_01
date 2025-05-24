
import numpy as np
import matplotlib.pyplot as plt

# --------------------------
# 1. исходные параметры
# --------------------------
U0, U1 = 0.5, 4.5                 # лог.0 и лог.1
t_max   = 1e-3                    # 1 мс
h       = 1e-6                    # шаг 1 мкс
t       = np.arange(0, t_max, h)  # временная шкала

freqs   = [5e3, 10e3]             # 5 кГц и 10 кГц
T1, T2  = 1e-5, 2e-5              # две «RC»-константы
A1, A2  = 0.1, 0.3                # амплитуды помех
zones   = [(1.5, 3.5), (2.0, 4.0)]# запрещённые зоны

# --------------------------
# 2. генератор меандра
# --------------------------
def meander(f):
    period = 1 / f
    return np.where((t % period) < (period / 2), U1, U0)

# --------------------------
# 3. RC-фильтр (метод Эйлера)
# --------------------------
def rc_filter(y, T):
    u = np.zeros_like(y)
    for n in range(len(y) - 1):
        u[n+1] = u[n] + h * (y[n] - u[n]) / T
    return u

# --------------------------
# 4. добавление помехи
# --------------------------
rng = np.random.default_rng()

def add_noise(u, A):
    return u + rng.uniform(-A, A, size=u.shape)

# --------------------------
# 5. логический каскад (гистерезис)
# --------------------------
def logic_out(u, umin, umax):
    out = np.zeros_like(u)
    out[0] = 0  # стартуем с лог.0
    for n in range(len(u) - 1):
        if   out[n]==0 and u[n] > umax: out[n+1] = 1
        elif out[n]==1 and u[n] < umin: out[n+1] = 0
        else:                           out[n+1] = out[n]
    return out

# --------------------------------------------------------------
# 6. строим графики сразу для двух частот, двух RC и двух шумов
# --------------------------------------------------------------
fig, ax = plt.subplots(5, 2, figsize=(12, 10), sharex=True)

for col, f in enumerate(freqs):
    # (1) чистый меандр
    y = meander(f)
    ax[0][col].plot(t*1e3, y); ax[0][col].set_title(f'{int(f/1e3)} кГц — вход')

    # (2) после RC-фильтра
    u = rc_filter(y, T1); ax[1][col].plot(t*1e3, u); ax[1][col].set_title('RC (T=10 µs)')
    u = rc_filter(y, T2); ax[2][col].plot(t*1e3, u); ax[2][col].set_title('RC (T=20 µs)')

    # (3) добавляем шум
    u_noise = add_noise(rc_filter(y, T1), A1)
    ax[3][col].plot(t*1e3, u_noise); ax[3][col].set_title('RC+noise (A=0.1)')

    # (4) логический выход (берём первую зону)
    out = logic_out(u_noise, *zones[0])
    ax[4][col].step(t*1e3, out, where='post'); ax[4][col].set_title('logic out')

for a in ax.flatten(): a.grid(True)
ax[-1][0].set_xlabel('Время, мкс'); ax[-1][1].set_xlabel('Время, мкс')
fig.tight_layout()
plt.show()
