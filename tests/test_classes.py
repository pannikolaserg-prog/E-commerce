import sys
import os
from io import StringIO
from unittest.mock import patch

# Добавляем src в путь Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.classes import Product, Category


def test_product_creation():
    """Тест создания товара"""
    p = Product("Телефон", "Смартфон", 10000, 5)
    assert p.name == "Телефон"
    assert p.description == "Смартфон"
    assert p.price == 10000
    assert p.quantity == 5


def test_product_price_getter():
    """Тест получения цены"""
    p = Product("Товар", "Описание", 500, 2)
    assert p.price == 500


def test_product_price_setter_positive():
    """Тест установки корректной цены"""
    p = Product("Товар", "Описание", 100, 1)
    p.price = 200
    assert p.price == 200


def test_product_price_setter_negative():
    """Тест защиты от отрицательной цены"""
    p = Product("Товар", "Описание", 100, 1)

    # Захватываем вывод в консоль
    captured_output = StringIO()
    sys.stdout = captured_output

    p.price = -50
    sys.stdout = sys.__stdout__  # Восстанавливаем stdout

    assert "Цена не должна быть нулевая или отрицательная" in captured_output.getvalue()
    assert p.price == 100  # Цена не изменилась


def test_product_price_setter_zero():
    """Тест защиты от нулевой цены"""
    p = Product("Товар", "Описание", 100, 1)

    captured_output = StringIO()
    sys.stdout = captured_output

    p.price = 0
    sys.stdout = sys.__stdout__

    assert "Цена не должна быть нулевая или отрицательная" in captured_output.getvalue()
    assert p.price == 100


def test_product_price_decrease_with_confirmation():
    """Тест понижения цены с подтверждением"""
    p = Product("Товар", "Описание", 100, 1)

    # Симулируем ввод 'y' для подтверждения
    with patch('builtins.input', return_value='y'):
        p.price = 80

    assert p.price == 80


def test_product_price_decrease_without_confirmation():
    """Тест понижения цены без подтверждения"""
    p = Product("Товар", "Описание", 100, 1)

    # Симулируем ввод 'n' для отказа
    with patch('builtins.input', return_value='n'):
        p.price = 80

    assert p.price == 100  # Цена не изменилась


def test_new_product_creation():
    """Тест создания товара через new_product"""
    data = {
        "name": "Ноутбук",
        "description": "Игровой",
        "price": 50000,
        "quantity": 3
    }

    p = Product.new_product(data)

    assert p.name == "Ноутбук"
    assert p.description == "Игровой"
    assert p.price == 50000
    assert p.quantity == 3


def test_new_product_with_duplicate():
    """Тест new_product с дубликатом товара"""
    existing_products = [Product("Телефон", "Старый", 8000, 10)]

    data = {
        "name": "Телефон",  # То же имя
        "description": "Новый",
        "price": 12000,  # Выше старой цены
        "quantity": 5
    }

    result = Product.new_product(data, existing_products)

    # Должен вернуть существующий товар
    assert result is existing_products[0]
    # Количество объединилось
    assert result.quantity == 15  # 10 + 5
    # Цена выбрана максимальная
    assert result.price == 12000


def test_new_product_with_duplicate_lower_price():
    """Тест new_product с дубликатом и более низкой ценой"""
    existing_products = [Product("Телефон", "Старый", 10000, 10)]

    data = {
        "name": "Телефон",
        "description": "Новый",
        "price": 8000,  # Ниже старой цены
        "quantity": 5
    }

    result = Product.new_product(data, existing_products)

    # Цена должна остаться старой (большей)
    assert result.price == 10000
    # Количество объединилось
    assert result.quantity == 15


def test_category_creation():
    """Тест создания категории"""
    cat = Category("Электроника", "Техника")

    assert cat.name == "Электроника"
    assert cat.description == "Техника"
    assert cat.product_count == 0


def test_category_creation_with_products():
    """Тест создания категории с товарами"""
    p1 = Product("Товар1", "Описание", 100, 1)
    p2 = Product("Товар2", "Описание", 200, 2)

    cat = Category("Категория", "Описание", [p1, p2])

    assert cat.product_count == 2
    assert len(cat.products) == 2


def test_add_product():
    """Тест добавления товара в категорию"""
    cat = Category("Тест", "Тест")
    p = Product("Товар", "Описание", 100, 5)

    cat.add_product(p)

    assert cat.product_count == 1
    assert len(cat.products) == 1


def test_add_wrong_product_type():
    """Тест добавления неправильного типа товара"""
    cat = Category("Тест", "Тест")

    captured_output = StringIO()
    sys.stdout = captured_output

    cat.add_product("не товар")
    sys.stdout = sys.__stdout__

    assert "Ошибка: можно добавлять только Product" in captured_output.getvalue()
    assert cat.product_count == 0


def test_products_getter_format():
    """Тест формата вывода товаров"""
    p = Product("Смартфон", "Описание", 15000, 3)
    cat = Category("Тест", "Описание", [p])

    products_info = cat.products

    assert len(products_info) == 1
    product_str = products_info[0]
    assert "Смартфон" in product_str
    assert "15000 руб." in product_str
    assert "Остаток: 3 шт." in product_str


def test_multiple_additions():
    """Тест множественных добавлений"""
    cat = Category("Тест", "Тест")

    for i in range(3):
        p = Product(f"Товар{i}", "Описание", 100 * (i + 1), i + 1)
        cat.add_product(p)

    assert cat.product_count == 3
    assert len(cat.products) == 3

    # Проверяем что все товары в списке
    for i in range(3):
        expected_str = f"Товар{i}, {100 * (i + 1)} руб. Остаток: {i + 1} шт."
        assert expected_str in cat.products


def test_empty_category():
    """Тест пустой категории"""
    cat = Category("Пустая", "Категория без товаров")

    assert cat.product_count == 0
    assert cat.products == []  # Пустой список
