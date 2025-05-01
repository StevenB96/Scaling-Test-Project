import os
from flask import Flask, request, jsonify
from pymongo import MongoClient, errors
from scraper import fetch_price  # Function to scrape price from the web
from celery_worker import check_prices  # Celery task for checking prices asynchronously

app = Flask(__name__)

# MongoDB setup with timeout and error handling
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")  # Changed default from 'mongos' to 'localhost'
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")  # Quick test to ensure MongoDB is reachable
    db = client["tracker"]
except errors.ServerSelectionTimeoutError as e:
    app.logger.error(f"Could not connect to MongoDB: {e}")
    db = None

# Health check or basic test route
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Hello World!"})

# Retrieve all tracked products
@app.route("/products", methods=["GET"])
def get_products():
    if db is None:
        return jsonify({"error": "Database unavailable"}), 500
    products = list(db.products.find({}, {"_id": 0}))
    return jsonify(products)

# Add a new product to be tracked
@app.route("/track", methods=["POST"])
def track_product():
    if db is None:
        return jsonify({"error": "Database unavailable"}), 500
    data = request.json
    db.products.insert_one(data)
    return jsonify({"message": "Product added"}), 201

# Trigger asynchronous price check using Celery
@app.route("/check", methods=["POST"])
def trigger_price_check():
    check_prices.delay()
    return jsonify({"message": "Price check triggered"})

# Entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
