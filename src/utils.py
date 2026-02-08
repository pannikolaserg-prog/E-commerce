import json
from typing import List

# Потом импорты проекта
from src.classes import Category, Product


def load_json_to_objects(json_path: str = "data/products.json") -> List[Category]:
    """
    Простая функция для загрузки данных из JSON файла
    и создания объектов классов Product и Category.
    Args:
        json_path (str): Путь к JSON файлу. По умолчанию "data/products.json"
    Returns:
        List[Category]: Список объектов Category
    """
    try:
        # Открываем и читаем JSON файл
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        categories = []

        # Проходим по всем категориям из JSON
        for category_data in data:
            # Создаем список товаров для категории
            products = []
            for product_data in category_data["products"]:
                # Создаем объект Product
                product = Product(
                    name=product_data["name"],
                    description=product_data["description"],
                    price=product_data["price"],
                    quantity=product_data["quantity"],
                )
                products.append(product)

            # Создаем объект Category
            category = Category(
                name=category_data["name"], description=category_data["description"], products=products
            )
            categories.append(category)

        print(f"Данные загружены из {json_path}")
        print(f"Категорий: {len(categories)}")
        print(f"Всего товаров: {sum(len(cat.products) for cat in categories)}")

        return categories

    except FileNotFoundError:
        print(f"Ошибка: файл {json_path} не найден")
        print("Убедитесь, что файл находится в папке data/")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {json_path} содержит некорректный JSON")
        return []
    except KeyError as e:
        print(f"Ошибка: в файле отсутствует поле {e}")
        return []
