import json
from pymongo import MongoClient

# Вставте сюди свій MongoDB URI
MONGO_URI = "mongodb+srv://bugz:QZjizq56F-3vA@cluster0.8xtucnd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client.quotes_db  # Назва вашої бази

# Завантаження з файлів
with open("authors.json", encoding="utf-8") as af:
    authors = json.load(af)

with open("quotes.json", encoding="utf-8") as qf:
    quotes = json.load(qf)

# Імпорт у колекції
db.authors.drop()
db.quotes.drop()

db.authors.insert_many(authors)
db.quotes.insert_many(quotes)

print("Дані імпортовано успішно.")