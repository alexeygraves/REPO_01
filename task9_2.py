import re

def remove_consecutive_duplicates(s):
    # Регулярное выражение для поиска повторяющихся слов
    pattern = r'\b(\w+)\s+\1\b'
    return re.sub(pattern, r'\1', s)

# Пример
some_string = 'Напишите функцию функцию, которая будет будет будет будет удалять все все все все последовательные повторы слов из из из из заданной строки строки при помощи регулярных выражений'
print(remove_consecutive_duplicates(some_string))
