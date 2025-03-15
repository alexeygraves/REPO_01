from datetime import datetime

# Функция для обработки входных данных
def process_date(date_str):
    # Попробуем все три возможных формата
    formats = [
        "%A, %B %d, %Y",      # The Moscow Times — Wednesday, October 2, 2002
        "%A, %d.%m.%y",       # The Guardian — Friday, 11.10.13
        "%A, %d %B %Y"        # Daily News — Thursday, 18 August 1977
    ]
    
    for date_format in formats:
        try:
            # Преобразуем строку в объект datetime
            return datetime.strptime(date_str, date_format)
        except ValueError:
            # Если не удалось преобразовать, продолжаем проверку с другим форматом
            continue
    # Если все форматы не подошли, выводим сообщение об ошибке
    raise ValueError(f"Неизвестный формат даты: {date_str}")

# Главная программа
def main():
    print("Введите дату в одном из следующих форматов:")
    print("1. The Moscow Times — Wednesday, October 2, 2002")
    print("2. The Guardian — Friday, 11.10.13")
    print("3. Daily News — Thursday, 18 August 1977")
    print("Для выхода введите 'exit'.")
    
    while True:
        # Ввод данных от пользователя
        user_input = input("Введите дату: ").strip()
        
        # Проверка на выход
        if user_input.lower() == 'exit':
            print("Завершение программы.")
            break
        
        try:
            # Обрабатываем введенную дату
            result = process_date(user_input)
            print(f"Дата в формате datetime: {result}")
        except ValueError as e:
            # Выводим ошибку, если формат даты не распознан
            print(e)

# Запуск программы
if __name__ == "__main__":
    main()
