import os
from celery import Celery
from pymongo import MongoClient
from scraper import fetch_price  # Function that scrapes the latest price from a product URL

# Get Redis and MongoDB URIs from environment variables
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")  # Default to Redis running in a container
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongos:27017")  # Default to Mongo router

# Initialize Celery app with Redis as the broker
app = Celery("tasks", broker=REDIS_URL)

# Define a Celery task to check product prices
@app.task
def check_prices():
    client = MongoClient(MONGO_URI)  # Connect to MongoDB
    db = client["tracker"]  # Use the 'tracker' database

    # Iterate through all tracked products
    for product in db.products.find():
        new_price = fetch_price(product["url"])  # Get the latest price using the scraper

        # If price has dropped, log it and update the database
        if new_price < product["price"]:
            print(f"Alert: {product['name']} dropped to {new_price}")
            db.products.update_one(
                {"url": product["url"]},       # Find product by URL
                {"$set": {"price": new_price}}  # Update price
            )
