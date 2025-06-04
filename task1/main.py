from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure, OperationFailure

client = MongoClient("mongodb://localhost:27017/")
db = client["cat_db"]
cats_collection = db["cats"]

def create_cat(name, age, features):
    try:
        cat = {"name": name, "age": age, "features": features}
        result = cats_collection.insert_one(cat)
        print(f"Кот створений з id: {result.inserted_id}")
    except Exception as e:
        print("Помилка створення:", e)

def show_all_cats():
    try:
        cats = cats_collection.find()
        for cat in cats:
            print(cat)
    except Exception as e:
        print("Помилка при читанні:", e)

def find_cat_by_name(name):
    try:
        cat = cats_collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"Кота з ім’ям {name} не знайдено.")
    except Exception as e:
        print("Помилка пошуку:", e)

def update_cat_age(name, new_age):
    try:
        result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count:
            print(f"Вік кота {name} оновлено.")
        else:
            print(f"Кота з ім’ям {name} не знайдено.")
    except Exception as e:
        print("Помилка оновлення:", e)

def add_feature_to_cat(name, feature):
    try:
        result = cats_collection.update_one(
            {"name": name},
            {"$addToSet": {"features": feature}}
        )
        if result.modified_count:
            print(f"Характеристику додано до кота {name}.")
        else:
            print(f"Кота з ім’ям {name} не знайдено.")
    except Exception as e:
        print("Помилка додавання характеристики:", e)

def delete_cat_by_name(name):
    try:
        result = cats_collection.delete_one({"name": name})
        if result.deleted_count:
            print(f"Кота {name} видалено.")
        else:
            print(f"Кота з ім’ям {name} не знайдено.")
    except Exception as e:
        print("Помилка видалення:", e)

def delete_all_cats():
    try:
        result = cats_collection.delete_many({})
        print(f"Видалено {result.deleted_count} записів.")
    except Exception as e:
        print("Помилка при видаленні всіх:", e)

def menu():
    while True:
        print("\n1. Додати кота")
        print("2. Показати всіх котів")
        print("3. Знайти кота за ім’ям")
        print("4. Оновити вік кота")
        print("5. Додати характеристику")
        print("6. Видалити кота")
        print("7. Видалити всіх котів")
        print("0. Вихід")

        choice = input("Вибір: ")

        if choice == "1":
            name = input("Ім'я: ")
            age = int(input("Вік: "))
            features = input("Через кому характеристики: ").split(",")
            create_cat(name, age, [f.strip() for f in features])
        elif choice == "2":
            show_all_cats()
        elif choice == "3":
            name = input("Ім'я кота: ")
            find_cat_by_name(name)
        elif choice == "4":
            name = input("Ім'я кота: ")
            new_age = int(input("Новий вік: "))
            update_cat_age(name, new_age)
        elif choice == "5":
            name = input("Ім'я кота: ")
            feature = input("Нова характеристика: ")
            add_feature_to_cat(name, feature)
        elif choice == "6":
            name = input("Ім'я кота: ")
            delete_cat_by_name(name)
        elif choice == "7":
            delete_all_cats()
        elif choice == "0":
            break
        else:
            print("Невірний вибір.")

if __name__ == "__main__":
    try:
        menu()
    except ConnectionFailure:
        print("Не вдалося підключитися до MongoDB.")