import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from scraper import fetch_price  # Function to scrape price from the web
from celery_worker import check_prices  # Celery task for checking prices asynchronously

app = Flask(__name__)

# Get MongoDB connection string from environment variable (default to mongos router)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongos:27017")
client = MongoClient(MONGO_URI)
db = client["tracker"]  # Use the "tracker" database

# Health check or basic test route
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Hello World!"})

# Retrieve all tracked products from the database
@app.route("/products", methods=["GET"])
def get_products():
    products = list(db.products.find({}, {"_id": 0}))  # Exclude MongoDB's default _id field
    return jsonify(products)

# Add a new product to be tracked
@app.route("/track", methods=["POST"])
def track_product():
    data = request.json  # Parse incoming JSON data
    db.products.insert_one(data)  # Insert product into MongoDB
    return jsonify({"message": "Product added"}), 201  # Return success response

# Trigger asynchronous price check using Celery
@app.route("/check", methods=["POST"])
def trigger_price_check():
    check_prices.delay()  # Send task to Celery worker
    return jsonify({"message": "Price check triggered"})

# Entry point for running the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Listen on all interfaces (required for Docker)
