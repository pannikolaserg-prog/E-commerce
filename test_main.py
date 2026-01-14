from main import Product, Category

class TestProduct:
    """Тесты для класса Product"""

    def test_product_initialization(self):
        """Тест корректности инициализации объекта Product"""
        # Arrange
        name = "Тестовый продукт"
        description = "Тестовое описание"
        price = 1000.0
        quantity = 5

        # Act
        product = Product(name, description, price, quantity)

        # Assert
        assert product.name == name, "Название продукта установлено неверно"
        assert product.description == description, "Описание продукта установлено неверно"
        assert product.price == price, "Цена продукта установлена неверно"
        assert product.quantity == quantity, "Количество продукта установлено неверно"

    def test_product_attributes_types(self):
        """Тест типов атрибутов Product"""
        product = Product("Тест", "Описание", 500.0, 10)

        assert isinstance(product.name, str), "name должен быть строкой"
        assert isinstance(product.description, str), "description должен быть строкой"
        assert isinstance(product.price, float), "price должен быть float"
        assert isinstance(product.quantity, int), "quantity должен быть int"

    def test_product_with_different_data(self):
        """Тест создания продуктов с разными данными"""
        # Тест 1: Продукт с целой ценой
        product1 = Product("Продукт 1", "Описание 1", 100, 1)
        assert product1.price == 100

        # Тест 2: Продукт с дробной ценой
        product2 = Product("Продукт 2", "Описание 2", 99.99, 10)
        assert product2.price == 99.99

        # Тест 3: Продукт с нулевым количеством
        product3 = Product("Продукт 3", "Описание 3", 50.0, 0)
        assert product3.quantity == 0


class TestCategory:
    """Тесты для класса Category"""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_initialization(self):
        """Тест корректности инициализации объекта Category"""
        # Arrange
        name = "Тестовая категория"
        description = "Тестовое описание категории"
        products = [
            Product("П1", "Описание 1", 100.0, 1),
            Product("П2", "Описание 2", 200.0, 2)
        ]


        # Act
        category = Category(name, description, products)

        # Assert
        assert category.name == name, "Название категории установлено неверно"
        assert category.description == description, "Описание категории установлено неверно"
        assert category.products == products, "Список продуктов установлен неверно"
        assert len(category.products) == 2, "Неверное количество продуктов в категории"

    def test_category_counting(self):
        """Тест подсчета количества категорий"""
        # Проверяем начальное состояние
        assert Category.category_count == 0

        # Создаем первую категорию
        category1 = Category("Кат1", "Описание", [])
        assert Category.category_count == 1, "Счетчик категорий должен увеличиться до 1"

        # Создаем вторую категорию
        category2 = Category("Кат2", "Описание", [])
        assert Category.category_count == 2, "Счетчик категорий должен увеличиться до 2"

        # Создаем третью категорию
        category3 = Category("Кат3", "Описание", [])
        assert Category.category_count == 3, "Счетчик категорий должен увеличиться до 3"

    def test_product_counting(self):
        """Тест подсчета количества продуктов"""
        # Проверяем начальное состояние
        assert Category.product_count == 0

        # Создаем категорию с 2 продуктами
        p1 = Product("П1", "Описание", 100.0, 1)
        p2 = Product("П2", "Описание", 200.0, 2)
        category1 = Category("Кат1", "Описание", [p1, p2])

        assert Category.product_count == 2, f"Ожидалось 2 продукта, получено {Category.product_count}"

        # Создаем вторую категорию с 1 продуктом
        p3 = Product("П3", "Описание", 300.0, 3)
        category2 = Category("Кат2", "Описание", [p3])

        assert Category.product_count == 3, f"Ожидалось 3 продукта, получено {Category.product_count}"

        # Создаем третью категорию с 3 продуктами
        p4 = Product("П4", "Описание", 400.0, 4)
        p5 = Product("П5", "Описание", 500.0, 5)
        p6 = Product("П6", "Описание", 600.0, 6)
        category3 = Category("Кат3", "Описание", [p4, p5, p6])

        assert Category.product_count == 6, f"Ожидалось 6 продуктов, получено {Category.product_count}"