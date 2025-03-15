# Функция для вычисления минимального количества разломов
def min_breaks(n, m, memo={}):
    # Если одна из сторон шоколадки равна 1, количество разломов равно другой стороне - 1
    if n == 1 and m == 1:
        return 0
    if n == 1 or m == 1:
        return max(n, m) - 1
    
    # Проверка на наличие уже рассчитанного значения в кэше
    if (n, m) in memo:
        return memo[(n, m)]
    
    # Рекурсивно разломаем шоколадку по вертикали и горизонтали
    # Разделяем по вертикали
    vertical = min_breaks(n, m // 2, memo) + min_breaks(n, m - m // 2, memo) + 1
    # Разделяем по горизонтали
    horizontal = min_breaks(n // 2, m, memo) + min_breaks(n - n // 2, m, memo) + 1
    
    # Выбираем минимальное количество разломов
    result = min(vertical, horizontal)
    
    # Сохраняем результат в кэше
    memo[(n, m)] = result
    
    return result

# Пример
print(min_breaks(2, 3))  # Должно вывести 5
print(min_breaks(3, 3))  # Должно вывести 8
print(min_breaks(1, 1))  # Должно вывести 0
