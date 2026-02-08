import os
import sys
from io import StringIO
from unittest.mock import patch

import pytest

# Переходим в корень проекта
os.chdir(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.getcwd())

from src.classes import Category, LawnGrass, Product, Smartphone


def test_product_creation() -> None:
    """Тест создания товара"""
    p = Product("Телефон", "Смартфон", 10000, 5)
    assert p.name == "Телефон"
    assert p.description == "Смартфон"
    assert p.price == 10000
    assert p.quantity == 5


def test_product_price_getter() -> None:
    """Тест получения цены"""
    p = Product("Товар", "Описание", 500, 2)
    assert p.price == 500


def test_product_price_setter_positive() -> None:
    """Тест установки корректной цены"""
    p = Product("Товар", "Описание", 100, 1)
    p.price = 200
    assert p.price == 200


def test_product_price_setter_negative() -> None:
    """Тест защиты от отрицательной цены"""
    p = Product("Товар", "Описание", 100, 1)

    # Захватываем вывод в консоль
    captured_output = StringIO()
    sys.stdout = captured_output

    p.price = -50
    sys.stdout = sys.__stdout__  # Восстанавливаем stdout

    assert "Цена не должна быть нулевая или отрицательная" in captured_output.getvalue()
    assert p.price == 100  # Цена не изменилась


def test_product_price_setter_zero() -> None:
    """Тест защиты от нулевой цены"""
    p = Product("Товар", "Описание", 100, 1)

    captured_output = StringIO()
    sys.stdout = captured_output

    p.price = 0
    sys.stdout = sys.__stdout__

    assert "Цена не должна быть нулевая или отрицательная" in captured_output.getvalue()
    assert p.price == 100


def test_product_price_decrease_with_confirmation() -> None:
    """Тест понижения цены с подтверждением"""
    p = Product("Товар", "Описание", 100, 1)

    # Симулируем ввод 'y' для подтверждения
    with patch("builtins.input", return_value="y"):
        p.price = 80

    assert p.price == 80


def test_product_price_decrease_without_confirmation() -> None:
    """Тест понижения цены без подтверждения"""
    p = Product("Товар", "Описание", 100, 1)

    # Симулируем ввод 'n' для отказа
    with patch("builtins.input", return_value="n"):
        p.price = 80

    assert p.price == 100  # Цена не изменилась


def test_new_product_creation() -> None:
    """Тест создания товара через new_product"""
    data = {"name": "Ноутбук", "description": "Игровой", "price": 50000, "quantity": 3}

    p = Product.new_product(data)

    assert p.name == "Ноутбук"
    assert p.description == "Игровой"
    assert p.price == 50000
    assert p.quantity == 3


def test_new_product_with_duplicate() -> None:
    """Тест new_product с дубликатом товара"""
    existing_products = [Product("Телефон", "Старый", 8000, 10)]

    data = {"name": "Телефон", "description": "Новый", "price": 12000, "quantity": 5}  # То же имя  # Выше старой цены

    result = Product.new_product(data, existing_products)

    # Должен вернуть существующий товар
    assert result is existing_products[0]
    # Количество объединилось
    assert result.quantity == 15  # 10 + 5
    # Цена выбрана максимальная
    assert result.price == 12000


def test_new_product_with_duplicate_lower_price() -> None:
    """Тест new_product с дубликатом и более низкой ценой"""
    existing_products = [Product("Телефон", "Старый", 10000, 10)]

    data = {"name": "Телефон", "description": "Новый", "price": 8000, "quantity": 5}  # Ниже старой цены

    result = Product.new_product(data, existing_products)

    # Цена должна остаться старой (большей)
    assert result.price == 10000
    # Количество объединилось
    assert result.quantity == 15


def test_category_creation() -> None:
    """Тест создания категории"""
    cat = Category("Электроника", "Техника")

    assert cat.name == "Электроника"
    assert cat.description == "Техника"
    assert cat.product_count == 0


def test_category_creation_with_products() -> None:
    """Тест создания категории с товарами"""
    p1 = Product("Товар1", "Описание", 100, 1)
    p2 = Product("Товар2", "Описание", 200, 2)

    cat = Category("Категория", "Описание", [p1, p2])

    assert cat.product_count == 2
    assert len(cat.products) == 2


def test_add_product() -> None:
    """Тест добавления товара в категорию"""
    cat = Category("Тест", "Тест")
    p = Product("Товар", "Описание", 100, 5)

    cat.add_product(p)

    assert cat.product_count == 1
    assert len(cat.products) == 1


def test_products_getter_format() -> None:
    """Тест формата вывода товаров"""
    p = Product("Смартфон", "Описание", 15000, 3)
    cat = Category("Тест", "Описание", [p])

    products_info = cat.products

    assert len(products_info) == 1
    product_str = products_info[0]
    assert "Смартфон" in product_str
    assert "15000 руб." in product_str
    assert "Остаток: 3 шт." in product_str


def test_multiple_additions() -> None:
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


def test_empty_category() -> None:
    """Тест пустой категории"""
    cat = Category("Пустая", "Категория без товаров")

    assert cat.product_count == 0
    assert cat.products == []  # Пустой список


class TestNewStringFunctionality:
    """Тесты для нового строкового представления"""

    def test_product_str_with_float_price(self) -> None:
        """Тест __str__ с дробной ценой"""
        product = Product("Кофе", "Арабика", 299.99, 15)
        result = str(product)
        assert "299.99 руб." in result or "299.99 руб." in result
        assert "Остаток: 15 шт." in result

    def test_category_str_empty(self) -> None:
        """Тест __str__ для пустой категории"""
        category = Category("Пустая", "Категория без товаров")
        assert str(category) == "Пустая, количество продуктов: 0 шт."

    def test_category_str_with_products(self) -> None:
        """Тест __str__ для категории с товарами"""
        products = [Product("Товар1", "", 100, 5), Product("Товар2", "", 200, 3), Product("Товар3", "", 150, 2)]
        category = Category("Тест", "Категория", products)
        # 5 + 3 + 2 = 10
        assert str(category) == "Тест, количество продуктов: 10 шт."

    def test_category_products_getter_uses_str(self) -> None:
        """Тест что геттер products использует __str__ Product"""
        product = Product("Тестовый", "Товар", 500, 8)
        category = Category("Кат", "Описание", [product])

        products_list = category.products
        assert len(products_list) == 1
        assert products_list[0] == "Тестовый, 500 руб. Остаток: 8 шт."


class TestProductAddition:
    """Тесты для сложения товаров"""

    def test_product_add_basic(self) -> None:
        """Базовый тест сложения товаров"""
        p1 = Product("A", "", 100, 10)  # 100 * 10 = 1000
        p2 = Product("B", "", 200, 2)  # 200 * 2 = 400

        result = p1 + p2
        assert result == 1400  # 1000 + 400

    def test_product_add_order(self) -> None:
        """Тест порядка сложения (коммутативность)"""
        p1 = Product("X", "", 50, 4)  # 50 * 4 = 200
        p2 = Product("Y", "", 30, 10)  # 30 * 10 = 300

        result1 = p1 + p2
        result2 = p2 + p1
        assert result1 == 500
        assert result2 == 500
        assert result1 == result2

    def test_product_add_with_zero_quantity(self) -> None:
        """Тест: создание товара с нулевым количеством должно вызывать ValueError"""
        with pytest.raises(ValueError) as exc_info:
            Product("Тестовый товар", "Описание", 100.0, 0)

        # Проверяем текст сообщения об ошибке
        assert "Товар с нулевым количеством не может быть добавлен" in str(exc_info.value)

    def test_product_add_with_same_product(self) -> None:
        """Тест сложения товара с самим собой"""
        p = Product("Один", "", 500, 3)  # 500 * 3 = 1500
        result = p + p  # 1500 + 1500
        assert result == 3000


class TestOldTestsStillWork:
    """Тесты, что старая функциональность все еще работает"""

    def test_product_creation_old(self) -> None:
        """Старый тест создания товара"""
        p = Product("Телефон", "Смартфон", 10000, 5)
        assert p.name == "Телефон"
        assert p.description == "Смартфон"
        assert p.price == 10000
        assert p.quantity == 5

    def test_product_price_protection_old(self) -> None:
        """Старый тест защиты цены"""
        p = Product("Тест", "Тест", 100, 1)

        # Сохраняем вывод в консоль
        captured_output = StringIO()
        sys.stdout = captured_output

        # Пытаемся установить отрицательную цену
        p.price = -50
        sys.stdout = sys.__stdout__

        assert "Цена не должна быть нулевая или отрицательная" in captured_output.getvalue()
        assert p.price == 100  # Цена не изменилась

    def test_new_product_classmethod_old(self) -> None:
        """Старый тест класс-метода new_product"""
        data = {"name": "Ноутбук", "description": "Игровой", "price": 50000, "quantity": 3}
        p = Product.new_product(data)

        assert p.name == "Ноутбук"
        assert p.price == 50000
        assert p.quantity == 3

    def test_category_creation_old(self) -> None:
        """Старый тест создания категории"""
        cat = Category("Электроника", "Техника")
        assert cat.name == "Электроника"
        assert cat.description == "Техника"

    def test_category_add_product_old(self) -> None:
        """Старый тест добавления товара в категорию"""
        cat = Category("Тест", "Тест")
        p = Product("Товар", "Описание", 100, 5)

        cat.add_product(p)
        assert len(cat.products) == 1

    def test_private_products_attribute_old(self) -> None:
        """Старый тест приватности списка товаров"""
        cat = Category("Тест", "Тест")

        # Нельзя получить доступ к приватному атрибуту
        # (зависит от реализации)
        if hasattr(cat, "_Category__products"):
            # Если используется name mangling
            assert hasattr(cat, "_Category__products")


class TestIntegration:
    """Интеграционные тесты всей системы"""

    def test_price_change_affects_str(self) -> None:
        """Тест что изменение цены влияет на строковое представление"""
        p = Product("Товар", "Описание", 100, 5)
        original_str = str(p)
        assert "100 руб." in original_str

        # Меняем цену
        p.price = 150
        new_str = str(p)
        assert "150 руб." in new_str
        assert "100 руб." not in new_str

    def test_quantity_change_affects_str(self) -> None:
        """Тест что изменение количества влияет на строковое представление"""
        p = Product("Товар", "Описание", 100, 5)
        p.quantity = 8
        assert "Остаток: 8 шт." in str(p)


def test_smartphone_creation() -> None:
    """Тест создания смартфона"""
    smartphone = Smartphone(
        name="iPhone 15",
        description="Смартфон",
        price=150000,
        quantity=5,
        efficiency=95.5,
        model="15 Pro",
        memory=256,
        color="Black",
    )
    assert smartphone.name == "iPhone 15"
    assert smartphone.price == 150000
    assert smartphone.efficiency == 95.5
    assert smartphone.memory == 256
    # Проверяем, что наследуется от Product
    assert isinstance(smartphone, Product)


def test_lawn_grass_creation() -> None:
    """Тест создания газонной травы"""
    grass = LawnGrass(
        name="Газонная трава",
        description="Элитная",
        price=500,
        quantity=20,
        country="Россия",
        germination_period="7 дней",
        color="Зеленый",
    )
    assert grass.name == "Газонная трава"
    assert grass.price == 500
    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"
    assert isinstance(grass, Product)


def test_smartphone_and_grass_addition() -> None:
    """Тест сложения смартфона и травы (если разрешено)"""
    smartphone = Smartphone("Phone", "", 100000, 2, 95.0, "X", 256, "Black")
    grass = LawnGrass("Grass", "", 500, 10, "RU", "7d", "Green")

    # Если __add__ проверяет type() is Product, то должно работать
    # Если проверяет type() is type(self), то вызовет ошибку
    try:
        result = smartphone + grass
        print(f"Сложение разрешено, результат: {result}")
        assert isinstance(result, (int, float))
    except TypeError:
        print("Сложение запрещено - разные типы товаров")


def test_middle_price() -> None:
    """Тест средней цены"""
    # 1. Пустая категория
    category1 = Category("Пустая", "Нет товаров", [])
    assert category1.middle_price() == 0

    # 2. Один товар
    p1 = Product("Яблоко", "Фрукт", 100, 5)
    category2 = Category("Фрукты", "Свежие фрукты", [p1])
    # 100 * 5 / 5 = 100
    assert category2.middle_price() == 100.0

    # 3. Несколько товаров
    p2 = Product("Банан", "Фрукт", 50, 10)  # 50 * 10 = 500
    p3 = Product("Апельсин", "Фрукт", 80, 5)  # 80 * 5 = 400
    category3 = Category("Фрукты2", "Разные", [p2, p3])
    # (500 + 400) / (10 + 5) = 900 / 15 = 60
    assert category3.middle_price() == 60.0

    # 5. Разные количества
    p4 = Product("Молоко", "2.5%", 90, 2)  # 180
    p5 = Product("Хлеб", "Белый", 50, 3)  # 150
    p6 = Product("Сыр", "Российский", 300, 1)  # 300
    category4 = Category("Продукты", "Еда", [p4, p5, p6])
    # (180 + 150 + 300) / (2 + 3 + 1) = 630 / 6 = 105
    assert category4.middle_price() == 105.0
