import re

def validate_car_number(car_id):
    # Регулярное выражение для проверки транспортного номера
    pattern = r'^[А-Я]{1}[0-9]{3}[А-Я]{2}[0-9]{2,3}$'
    
    if re.match(pattern, car_id):
        # Если номер валиден, разделим его на номер и регион
        car_number = car_id[:5]  # Первая часть - номер
        region = car_id[5:]  # Последняя часть - регион
        return f"Номер {car_number} валиден. Регион: {region}."
    else:
        return "Номер не валиден."

# Примеры
print(validate_car_number('А222BС96'))  # Номер А222BС валиден. Регион: 96.
print(validate_car_number('АБ22ВВ193'))  # Номер не валиден.
