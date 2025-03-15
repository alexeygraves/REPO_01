# Задание 1: Средняя буква или две средних буквы

def middle_letters(word):
    # Находим длину слова
    length = len(word)
    
    # Если длина нечётная, выводим одну среднюю букву
    if length % 2 != 0:
        middle = word[length // 2]
    else:
        # Если длина чётная, выводим две средних буквы
        middle = word[length // 2 - 1:length // 2 + 1]
    
    return middle

# Примеры
word1 = 'test'
word2 = 'testing'

print(f"Для слова '{word1}' средняя буква: {middle_letters(word1)}")
print(f"Для слова '{word2}' средняя буква: {middle_letters(word2)}")
