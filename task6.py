import csv

def process_log_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile, \
         open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        
        # Создание CSV reader и writer
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Записываем заголовок в новый файл
        writer.writerow(['user_id', 'source', 'category'])
        
        # Обрабатываем строки файла
        for row in reader:
            user_id, source, purchase_info = row  # Предполагаем, что файл имеет структуру (user_id, source, purchase_info)
            
            # Проверяем, если покупка была, то добавляем категорию
            if purchase_info:
                # В данном примере условие покупки и категории может быть любое (например, категория по умолчанию 'Продукты')
                category = "Продукты"  # Здесь можно добавить логику для определения категории покупки
                writer.writerow([user_id, source, category])  # Записываем данные с категорией
            else:
                continue

# Пример использования функции
input_file = 'visit_log.csv'
output_file = 'funnel.csv'
process_log_file(input_file, output_file)
