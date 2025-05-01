import os
import logging
from celery import Celery
from pymongo import MongoClient, errors
from scraper import fetch_price  # Function that scrapes the latest price from a product URL

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get Redis and MongoDB URIs from environment variables
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")  # Default to Redis running in a container
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongos:27017")  # Default to Mongo router

# Initialize Celery app with Redis as the broker
app = Celery("tasks", broker=REDIS_URL)

# Define a Celery task to check product prices
@app.task
def check_prices():
    try:
        logger.info(f"Connecting to MongoDB at {MONGO_URI}")
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # Connect to MongoDB
        client.admin.command("ping")  # Test MongoDB connection
        db = client["tracker"]  # Use the 'tracker' database
        logger.info("Connected to MongoDB successfully.")
    except errors.ServerSelectionTimeoutError as e:
        logger.error(f"MongoDB connection failed: {e}")
        return
    except Exception as e:
        logger.error(f"Unexpected error connecting to MongoDB: {e}")
        return

    # Iterate through all tracked products
    for product in db.products.find():
        try:
            logger.debug(f"Checking price for {product['name']} ({product['url']})")
            new_price = fetch_price(product["url"])  # Get the latest price using the scraper
            logger.debug(f"Current price: {product['price']}, New price: {new_price}")

            # If price has dropped, log it and update the database
            if new_price < product["price"]:
                logger.info(f"Alert: {product['name']} dropped to {new_price}")
                db.products.update_one(
                    {"url": product["url"]},       # Find product by URL
                    {"$set": {"price": new_price}}  # Update price
                )
        except Exception as e:
            logger.error(f"Error checking product '{product.get('name', 'unknown')}': {e}")
