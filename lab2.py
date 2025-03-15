# Программа для расчета экономии на покупках в разных магазинах

def get_product_prices():
    """Функция для ввода товаров и их цен в разных магазинах."""
    products = {}
    while True:
        product_name = input("Введите название товара (или 'stop' для завершения): ")
        if product_name.lower() == 'stop':
            break
        prices = {}
        while True:
            store_name = input("Введите название магазина (или 'stop' для завершения): ")
            if store_name.lower() == 'stop':
                break
            price = float(input(f"Введите цену товара '{product_name}' в магазине '{store_name}': "))
            prices[store_name] = price
        products[product_name] = prices
    return products

def calculate_total_cost(products):
    """Функция для расчета общей стоимости покупок в каждом магазине."""
    total_cost = {}
    for product, stores in products.items():
        for store, price in stores.items():
            if store not in total_cost:
                total_cost[store] = 0
            total_cost[store] += price
    return total_cost

def find_best_store(total_cost):
    """Функция для поиска магазина, где можно сэкономить больше всего."""
    best_store = min(total_cost, key=total_cost.get)
    return best_store, total_cost[best_store]

def main():
    """Главная функция программы."""
    print("Добро пожаловать в программу для сравнения цен!")
    products = get_product_prices()
    total_cost = calculate_total_cost(products)
    
    # Выводим общую стоимость покупок в каждом магазине
    print("\nОбщая стоимость покупок в каждом магазине:")
    for store, cost in total_cost.items():
        print(f"{store}: {cost:.2f} руб.")
    
    # Находим магазин с наибольшей экономией
    best_store, best_price = find_best_store(total_cost)
    print(f"\nМагазин с наибольшей экономией: {best_store} с ценой {best_price:.2f} руб.")

if __name__ == "__main__":
    main()
