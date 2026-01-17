from itertools import product


class Product:
    """Класс для описания продуктов"""

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
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
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Проверяем, есть ли текущая цена
        current_price = getattr(self, '_Product__price', None)

        if current_price is not None and new_price < current_price:
            answer = input(f"Цена понижается с {current_price} до {new_price}. Подтвердить (y/n)? ")
            if answer.lower() != 'y':
                print("Изменение цены отменено")
                return

        self.__price = new_price


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
        result = []
        template = "{name}, {price} руб. Остаток: {quantity} шт."

        for p in self.__products:
            item = template.format(
                name=p.name,
                price=p.price,
                quantity=p.quantity
            )
            result.append(item)

        return result

    @property
    def product_count(self):
        return len(self.__products)
