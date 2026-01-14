from itertools import product


class Product:
    """Класс для описания продуктов"""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс для категории продуктов"""

    name: str
    description: str
    products: list[product]

    # Счетчики на уровне класса
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = products

        # Увеличиваем счетчики при создании новой категории
        Category.category_count += 1
        Category.product_count += len(products)
