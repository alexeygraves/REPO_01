import time
import threading

# Формулы
def formula1(x):
    return x**2 - x**2 + x**4 - x**5 + x + x

def formula2(x):
    return x + x

def compute_step1(iterations):
    result = 0
    for i in range(iterations):
        result += formula1(i)
    return result

def compute_step2(iterations):
    result = 0
    for i in range(iterations):
        result += formula2(i)
    return result

def compute_step3(result1, result2):
    return result1 + result2

# Функция для многопоточного выполнения
def run_threads(iterations):
    start_time = time.time()

    # Создание потоков
    thread1 = threading.Thread(target=compute_step1, args=(iterations,))
    thread2 = threading.Thread(target=compute_step2, args=(iterations,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    # Время выполнения для вычислений шагов 1 и 2
    step1_duration = time.time() - start_time
    step2_duration = time.time() - start_time

    # Вычисление для шага 3
    result1 = compute_step1(iterations)
    result2 = compute_step2(iterations)
    result3 = compute_step3(result1, result2)

    # Время для шага 3
    step3_duration = time.time() - start_time

    print(f"Step 1 Duration (s): {step1_duration}")
    print(f"Step 2 Duration (s): {step2_duration}")
    print(f"Step 3 Duration (s): {step3_duration}")
    print(f"Result of Step 3: {result3}")

# Запуск вычислений на 10 000 и 100 000 итераций
run_threads(10000)
run_threads(100000)
