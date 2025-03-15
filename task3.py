# Исходные данные
items = {
    'milk15': {'name': 'молоко 1.5%', 'count': 34, 'price': 89.9},
    'cheese': {'name': 'сыр молочный 1 кг.', 'count': 12, 'price': 990.9},
    'sausage': {'name': 'колбаса 1 кг.', 'count': 122, 'price': 1990.9}
}

# Создаём словарь с использованием dict comprehension
price_less_20 = {key: value['count'] < 20 for key, value in items.items()}

# Выводим результат
print(price_less_20)
