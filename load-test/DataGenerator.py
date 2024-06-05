import random
from faker import Faker
from pymongo import MongoClient

# Initialize Faker
fake = Faker()

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce']
products_collection = db['products']
users_collection = db['users']
orders_collection = db['orders']
reviews_collection = db['reviews']

# Generate Product Data
def generate_product_data(n):
    products = []
    for _ in range(n):
        product = {
            "name": fake.word(),
            "description": fake.text(),
            "price": round(random.uniform(10, 1000), 2),
            "category": fake.word(),
            "stock": random.randint(1, 100),
            "rating": round(random.uniform(1, 5), 1),
            "reviews": random.randint(0, 100)
        }
        products.append(product)
    return products

# Generate User Data
def generate_user_data(n):
    users = []
    for _ in range(n):
        user = {
            "name": fake.name(),
            "email": fake.email(),
            "password": fake.password(),
            "address": fake.address(),
            "phone": fake.phone_number(),
            "registered_at": fake.date_time_this_decade()
        }
        users.append(user)
    return users

# Generate Order Data
def generate_order_data(n, user_ids, product_ids):
    orders = []
    for _ in range(n):
        order = {
            "user_id": random.choice(user_ids),
            "products": [
                {"product_id": random.choice(product_ids), "quantity": random.randint(1, 5)}
                for _ in range(random.randint(1, 5))
            ],
            "total_amount": round(random.uniform(20, 500), 2),
            "status": random.choice(["pending", "completed", "shipped", "delivered"]),
            "ordered_at": fake.date_time_this_year()
        }
        orders.append(order)
    return orders

# Generate Review Data
def generate_review_data(n, user_ids, product_ids):
    reviews = []
    for _ in range(n):
        review = {
            "user_id": random.choice(user_ids),
            "product_id": random.choice(product_ids),
            "rating": random.randint(1, 5),
            "comment": fake.text(),
            "reviewed_at": fake.date_time_this_year()
        }
        reviews.append(review)
    return reviews

# Insert generated data into MongoDB
def insert_data_to_mongo():
    products = generate_product_data(100000)
    product_ids = products_collection.insert_many(products).inserted_ids
    
    users = generate_user_data(100000)
    user_ids = users_collection.insert_many(users).inserted_ids

    orders = generate_order_data(500000, user_ids, product_ids)
    orders_collection.insert_many(orders)
    
    reviews = generate_review_data(300000, user_ids, product_ids)
    reviews_collection.insert_many(reviews)

if __name__ == "__main__":
    insert_data_to_mongo()
    print("Data generation and insertion complete!")
