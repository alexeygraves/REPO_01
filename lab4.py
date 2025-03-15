import json
import xml.etree.ElementTree as ET

# Функция для конвертации JSON в XML
def json_to_xml(json_data):
    root = ET.Element("people")
    
    for person in json_data:
        person_element = ET.SubElement(root, "person")
        
        for key, value in person.items():
            sub_element = ET.SubElement(person_element, key)
            sub_element.text = str(value)
    
    tree = ET.ElementTree(root)
    return tree

# Чтение JSON файла
def read_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# Запись XML в файл
def write_xml_to_file(tree, filename):
    tree.write(filename, encoding='utf-8', xml_declaration=True)

# Основная программа
def main():
    # Читаем данные из JSON
    json_data = read_json_file("people.json")
    
    # Конвертируем в XML
    xml_tree = json_to_xml(json_data)
    
    # Записываем XML в файл
    write_xml_to_file(xml_tree, "people.xml")
    
    print("Конвертация завершена. Данные сохранены в 'people.xml'.")

if __name__ == "__main__":
    main()
