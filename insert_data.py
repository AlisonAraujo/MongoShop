from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime

user = "root"
passwd = "rios0410"
uri = f"mongodb://{user}:{passwd}@localhost:27017/?authSource=admin"
client = MongoClient(uri)
db = client["MongoShop"]
fake = Faker("pt_BR")

## declarando variaveis das collections
users = db.users
products = db.products
orders = db.orders

## Populando a collection Users ##
user_data = [
    {
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "cpf": fake.unique.cpf()
    }
    for i in range(100)
]
inserting_user_data = users.insert_many(user_data)
users_id = inserting_user_data.inserted_ids ##armazenando os IDs para atrelar ao pedido


## Populando a collection products ##
product_data = [
    {
        "name": fake.word().capitalize(),
        "description": fake.sentence(),
        "price": round(random.uniform(10,500),2),
        "stock": round(random.uniform(0,1000))
    }
    for i in range(50)
]
inserting_product_data = products.insert_many(product_data)

########################################################################

all_product_id = [doc["_id"] for doc in products.find({}, {"_id": 1})]
id_product = random.choice(all_product_id)
product_name = [doc["name"] for doc in products.find({"_id": id_product}, {"name": 1, "_id": 0})]
product_price = [doc["price"] for doc in products.find({"_id": id_product}, {"price": 1, "_id": 0})]

somar = round(
    product_price["price"] if isinstance(product_price, dict) else sum(p if isinstance(p, float) else p["price"] for p in product_price), 
    2
)

orders_data = [
    {
        "client_id": random.choice(users_id),
        "date": datetime.combine(fake.date_this_year(), datetime.min.time()),
        "product_id": id_product,
        "product_name": product_name,
        "product_price": product_price,
        "total": somar
    }
    for i in range(200)
]
inserting_orders_data = orders.insert_many(orders_data)
