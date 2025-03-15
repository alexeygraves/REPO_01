import time
import multiprocessing

def compute_step1_process(iterations):
    result = 0
    for i in range(iterations):
        result += formula1(i)
    return result

def compute_step2_process(iterations):
    result = 0
    for i in range(iterations):
        result += formula2(i)
    return result

def compute_step3_process(result1, result2):
    return result1 + result2

def run_processes(iterations):
    start_time = time.time()

    # Создание процессов
    process1 = multiprocessing.Process(target=compute_step1_process, args=(iterations,))
    process2 = multiprocessing.Process(target=compute_step2_process, args=(iterations,))

    process1.start()
    process2.start()

    process1.join()
    process2.join()

    # Время выполнения для вычислений шагов 1 и 2
    step1_duration = time.time() - start_time
    step2_duration = time.time() - start_time

    # Вычисление для шага 3
    result1 = compute_step1_process(iterations)
    result2 = compute_step2_process(iterations)
    result3 = compute_step3_process(result1, result2)

    # Время для шага 3
    step3_duration = time.time() - start_time

    print(f"Step 1 Duration (s): {step1_duration}")
    print(f"Step 2 Duration (s): {step2_duration}")
    print(f"Step 3 Duration (s): {step3_duration}")
    print(f"Result of Step 3: {result3}")

# Запуск вычислений на 10 000 и 100 000 итераций
run_processes(10000)
run_processes(100000)
