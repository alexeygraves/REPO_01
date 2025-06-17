
"""producer_consumer_shm.py

IPC «производитель–потребитель» через true shared‑memory (multiprocessing.shared_memory).
Работает на Python ≥ 3.8 без временных файлов, одинаково на Windows / Linux / macOS.
"""

import time
from multiprocessing import Process, shared_memory

BUF_SIZE = 1024
MSG      = b"Hello from shared_memory!\n"

def producer(name: str) -> None:
    shm = shared_memory.SharedMemory(name=name)
    buf = shm.buf
    print("[Producer] Writing...")
    buf[:len(MSG)] = MSG
    buf[len(MSG)]  = 0  # нуль‑терминатор
    shm.close()
    print("[Producer] Done.")

def consumer(name: str) -> None:
    shm = shared_memory.SharedMemory(name=name)
    buf = shm.buf
    print("[Consumer] Waiting data...")
    while buf[0] == 0:
        time.sleep(0.01)
    # читаем до нуль‑байта
    data = bytes(buf.tobytes().split(b"\x00", 1)[0])
    print("[Consumer] Received:", data.decode().strip())
    shm.close()

def main() -> None:
    # Создаём разделяемую память
    shm = shared_memory.SharedMemory(create=True, size=BUF_SIZE)
    shm.buf[:] = b"\x00" * BUF_SIZE   # обнуляем

    p_prod = Process(target=producer, args=(shm.name,))
    p_cons = Process(target=consumer,  args=(shm.name,))

    p_cons.start()
    p_prod.start()

    p_prod.join()
    p_cons.join()

    shm.close()
    shm.unlink()   # удаляем сегмент
    print("\n[Main] Finished.")

if __name__ == "__main__":
    main()
