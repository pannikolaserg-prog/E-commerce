import json
import os
import sys

# Переходим в корень проекта
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.getcwd())

from src.utils import load_json_to_objects


def test_load_json_file_not_found() -> None:
    """Тест загрузки при отсутствии файла"""
    categories = load_json_to_objects("несуществующий_файл.json")

    assert categories == [], "При отсутствии файла должен возвращаться пустой список"
    print("✅ test_load_json_file_not_found пройден")


def test_load_json_empty() -> None:
    """Тест загрузки пустого JSON"""
    # Создаем пустой JSON файл
    with open("empty.json", "w", encoding="utf-8") as f:
        json.dump([], f)

    categories = load_json_to_objects("empty.json")

    assert categories == [], "Пустой JSON должен возвращать пустой список"
    print("✅ test_load_json_empty пройден")

    os.remove("empty.json")
