from locust import HttpUser, TaskSet, task, between
from pymongo import MongoClient
import random

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce']
users_collection = db['users']

# Fetch users from MongoDB
users = list(users_collection.find({}, {"email": 1, "password": 1}))

class UserBehavior(TaskSet):
    def on_start(self):
        # Choose a random user from the list and log in
        self.user = random.choice(users)
        self.login()

    def login(self):
        response = self.client.post("/api/login", json={
            "email": self.user["email"],
            "password": self.user["password"]
        })
        if response.status_code == 200:
            self.user["token"] = response.json().get("token")

    @task(1)
    def view_products(self):
        self.client.get("/api/products")

    @task(2)
    def view_orders(self):
        if "token" in self.user:
            headers = {"Authorization": f"Bearer {self.user['token']}"}
            self.client.get("/api/orders", headers=headers)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)

if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py --host=http://localhost:8000")
