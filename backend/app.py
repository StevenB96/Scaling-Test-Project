import os
import logging
from flask import Flask, request, jsonify
from pymongo import MongoClient, errors
from celery_worker import check_prices

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = app.logger

# MongoDB setup with timeout and error handling
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")  # Changed default from 'mongos' to 'localhost'
try:
    logger.info(f"Connecting to MongoDB at {MONGO_URI}")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")  # Quick test to ensure MongoDB is reachable
    db = client["tracker"]  # Use the 'tracker' database
    logger.info("Successfully connected to MongoDB.")
except errors.ServerSelectionTimeoutError as e:
    logger.error(f"Could not connect to MongoDB: {e}")
    db = None

# Log every incoming request for debugging
@app.before_request
def log_request_info():
    logger.debug(f"Incoming {request.method} request to {request.path}")
    if request.method in ["POST", "PUT", "PATCH"]:
        logger.debug(f"Payload: {request.get_json()}")

# Health check or basic test route
@app.route("/test", methods=["GET"])
def test():
    logger.info("GET /test called")
    return jsonify({"message": "Hello World!"})

# Retrieve all tracked products
@app.route("/products", methods=["GET"])
def get_products():
    if db is None:
        logger.warning("Database unavailable when trying to fetch products")
        return jsonify({"error": "Database unavailable"}), 500
    try:
        products = list(db.products.find({}, {"_id": 0}))  # Exclude MongoDB's default _id field
        logger.debug(f"Retrieved {len(products)} products from the database")
        return jsonify(products)
    except Exception as e:
        logger.error(f"Error retrieving products: {e}")
        return jsonify({"error": "Failed to retrieve products"}), 500

# Add a new product to be tracked
@app.route("/track", methods=["POST"])
def track_product():
    if db is None:
        logger.warning("Database unavailable when trying to add a product")
        return jsonify({"error": "Database unavailable"}), 500
    try:
        data = request.json  # Parse incoming JSON data
        logger.debug(f"Inserting product data: {data}")
        db.products.insert_one(data)  # Insert product into MongoDB
        return jsonify({"message": "Product added"}), 201  # Return success response
    except Exception as e:
        logger.error(f"Error inserting product: {e}")
        return jsonify({"error": "Failed to add product"}), 500

# Trigger asynchronous price check using Celery
@app.route("/check", methods=["POST"])
def trigger_price_check():
    try:
        logger.info("Triggering price check task")
        check_prices.delay()  # Send task to Celery worker
        return jsonify({"message": "Price check triggered"})
    except Exception as e:
        logger.error(f"Failed to trigger price check: {e}")
        return jsonify({"error": "Failed to trigger price check"}), 500

# Entry point for running the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Listen on all interfaces (required for Docker)
