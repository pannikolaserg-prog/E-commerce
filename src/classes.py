from itertools import product


class Product:
    """Класс для описания продуктов"""

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data,  products_list=None):
        """Задание 3: класс-метод для создания товара"""
        name = product_data["name"]
        price = product_data["price"]
        quantity = product_data["quantity"]
        description = product_data["description"]

        # Проверка дубликатов (3*)
        if products_list:
            for prod in products_list:
                if prod.name.lower() == name.lower():
                    prod.quantity += quantity
                    if price > prod.price:
                        prod.price = price
                    return prod

        return cls(name, description, price, quantity)

    @property
    def price(self):
        """Задание 4: геттер для цены"""
        return self._price

    @price.setter
    def price(self, new_price):
        """Задание 4: сеттер для цены"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if hasattr(self, '_price') and new_price < self._price:
            answer = input(f"Цена понижается с {self._price} до {new_price}. Подтвердить (y/n)? ")
            if answer.lower() != 'y':
                return

        self._price = new_price


class Category:
    category_count = 0

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        # Задание 1: приватный список товаров
        self.__products = []

        if products:
            for p in products:
                self.add_product(p)

    def add_product(self, product):
        """Задание 1: метод для добавления товара"""
        if isinstance(product, Product):
            self.__products.append(product)
        else:
            print("Ошибка: можно добавлять только Product")

    @property
    def products(self):
        """Задание 2: геттер для списка товаров"""
        result = []
        for p in self.__products:
            result.append(f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт.")
        return result

    @property
    def product_count(self):
        return len(self.__products)
