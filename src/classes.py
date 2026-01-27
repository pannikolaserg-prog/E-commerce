class Product:
    """Класс для описания продуктов"""

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data, products_list=None):
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
        current_price = getattr(self, "_Product__price", None)

        if current_price is not None and new_price < current_price:
            answer = input(f"Цена понижается с {current_price} до {new_price}. Подтвердить (y/n)? ")
            if answer.lower() != "y":
                print("Изменение цены отменено")
                return

        self.__price = new_price

    def __str__(self):
        return f"({self.name}, {self.__price} руб. Остаток: {self.quantity} шт.)"

    def __add__(self, other):
        """
        Сложение товаров: возвращает общую стоимость всех товаров на складе
        Формула: (цена1 * количество1) + (цена2 * количество2)
        """
        if type(other) is type(self):
            return (self.price * self.quantity) + (other.price * other.quantity)
        else:
            raise TypeError("Можно складывать только объекты Product")


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
            raise TypeError("Ошибка: можно добавлять только Product")

    @property
    def products(self):
        result = []
        template = "{name}, {price} руб. Остаток: {quantity} шт."

        for p in self.__products:
            item = template.format(name=p.name, price=p.price, quantity=p.quantity)
            result.append(item)

        return result

    @property
    def product_count(self):
        return len(self.__products)

    @property
    def total_quantity(self):
        """Общее количество всех продуктов в категории"""
        return sum(p.quantity for p in self.__products)

    def __str__(self):
        """Задание 1: строковое отображение категории"""
        return f"{self.name}, количество продуктов: {self.total_quantity} шт."


class CategoryIterator:
    """Вспомогательный класс для итерации по товарам категории"""

    def __init__(self, category):
        """
        Инициализация итератора

        Args:
            category: объект класса Category
        """
        self.category = category
        self.products = category.products_objects  # Нужен метод для получения объектов
        self.index = 0

    def __iter__(self):
        """Возвращает сам объект как итератор"""
        self.index = 0
        return self

    def __next__(self):
        """Возвращает следующий товар из категории"""
        if self.index >= len(self.products):
            raise StopIteration
        product = self.products[self.index]
        self.index += 1
        return product


class Smartphone(Product):
    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
