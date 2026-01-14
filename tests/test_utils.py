import json
import os

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


def test_load_json_multiple_products():
    """Тест загрузки нескольких товаров в категории"""
    test_data = [
        {
            "name": "Категория",
            "description": "Описание",
            "products": [
                {"name": "Товар 1", "description": "Описание 1", "price": 100.0, "quantity": 5},
                {"name": "Товар 2", "description": "Описание 2", "price": 200.0, "quantity": 10},
                {"name": "Товар 3", "description": "Описание 3", "price": 300.0, "quantity": 15},
            ],
        }
    ]

    with open("multi_products.json", "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

    categories = load_json_to_objects("multi_products.json")

    assert len(categories) == 1
    assert len(categories[0].products) == 3
    assert categories[0].products[0].name == "Товар 1"
    assert categories[0].products[1].name == "Товар 2"
    assert categories[0].products[2].name == "Товар 3"

    print("✅ test_load_json_multiple_products пройден")

    os.remove("multi_products.json")


def test_product_attributes():
    """Тест правильности атрибутов товаров"""
    test_data = [
        {
            "name": "Категория",
            "description": "Описание",
            "products": [
                {"name": "Тестовый товар", "description": "Тестовое описание", "price": 1500.50, "quantity": 7}
            ],
        }
    ]

    with open("attrs.json", "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

    categories = load_json_to_objects("attrs.json")

    product = categories[0].products[0]

    assert product.name == "Тестовый товар"
    assert product.description == "Тестовое описание"
    assert product.price == 1500.50
    assert product.quantity == 7

    print("✅ test_product_attributes пройден")

    os.remove("attrs.json")


def test_category_counters():
    """Тест счетчиков категорий и товаров"""

    # Сбрасываем счетчики

    Category.category_count = 0
    Category.product_count = 0

    test_data = [
        {
            "name": "Категория 1",
            "description": "Описание 1",
            "products": [
                {"name": "Т1", "description": "Д1", "price": 100, "quantity": 1},
                {"name": "Т2", "description": "Д2", "price": 200, "quantity": 2},
            ],
        },
        {
            "name": "Категория 2",
            "description": "Описание 2",
            "products": [{"name": "Т3", "description": "Д3", "price": 300, "quantity": 3}],
        },
    ]

    with open("counters.json", "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

    categories = load_json_to_objects("counters.json")

    # Проверяем счетчики
    assert Category.category_count == 2, f"Должно быть 2 категории, а есть {Category.category_count}"
    assert Category.product_count == 3, f"Должно быть 3 товара, а есть {Category.product_count}"

    print(
        f"✅ test_category_counters пройден (категории: {Category.category_count}, товары: {Category.product_count})"
    )

    os.remove("counters.json")
