# Задание 2: Идеальные пары

def find_pairs(boys, girls):
    # Проверяем, чтобы количество мальчиков и девочек было одинаковым
    if len(boys) != len(girls):
        print("Внимание, кто-то может остаться без пары.")
        return
    
    # Сортируем списки имен по алфавиту
    boys.sort()
    girls.sort()

    # Создаём пары
    pairs = list(zip(boys, girls))
    
    print("Идеальные пары:")
    for boy, girl in pairs:
        print(f"{boy} и {girl}")

# Примеры
boys1 = ['Peter', 'Alex', 'John', 'Arthur', 'Richard']
girls1 = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']

boys2 = ['Peter', 'Alex', 'John', 'Arthur', 'Richard', 'Michael']
girls2 = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']

print("Пример 1:")
find_pairs(boys1, girls1)
print("\nПример 2:")
find_pairs(boys2, girls2)
