import json
import os
import sys

# Добавляем корень проекта в путь Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем ВСЕ модули сразу после добавления пути
from src.classes import Category
from src.utils import load_json_to_objects


def test_load_json_file_not_found():
    """Тест загрузки при отсутствии файла"""
    categories = load_json_to_objects("несуществующий_файл.json")

    assert categories == [], "При отсутствии файла должен возвращаться пустой список"
    print("✅ test_load_json_file_not_found пройден")


def test_load_json_empty():
    """Тест загрузки пустого JSON"""
    # Создаем пустой JSON файл
    with open("empty.json", "w", encoding="utf-8") as f:
        json.dump([], f)

    categories = load_json_to_objects("empty.json")

    assert categories == [], "Пустой JSON должен возвращать пустой список"
    print("✅ test_load_json_empty пройден")

    os.remove("empty.json")
