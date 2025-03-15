
# Задание 2: Проверка счастливого билета

number = 123321  # Пример номера билета

# Преобразуем номер билета в строку и извлекаем первые и последние три цифры
number_str = str(number)
first_half = sum(int(digit) for digit in number_str[:3])
second_half = sum(int(digit) for digit in number_str[3:])

if first_half == second_half:
    print("Счастливый билет")
else:
    print("Несчастливый билет")
