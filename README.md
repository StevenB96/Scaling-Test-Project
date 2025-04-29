# E-commerce Price Tracker (Sharded + Load-Balanced)

## Overview
This stack implements a price-tracking application that monitors product prices from e-commerce websites. The application is designed for scalability and high availability using:

- **Sharded MongoDB Cluster**: Two shards with a config server and a mongos router for horizontal scaling.
- **Flask API**: A backend REST API (Flask) for managing products and triggering price checks, running as two replicas behind an Nginx load balancer.
- **Celery Workers**: Two Celery worker services that scrape product prices asynchronously.
- **Frontend**: A simple static web app (HTML/JS) served by two Express.js servers, behind an Nginx load balancer.

## Components

### 1. MongoDB Sharded Cluster
- **Config Server (`configsvr`)**: Stores cluster metadata.
- **Shards (`shard1` & `shard2`)**: Store subsets of the data.
- **Mongos Router**: Routes client requests to the correct shard.

### 2. Flask Backend API
- **Services (`backend`, `backend2`)**: Handle product-related requests (viewing, tracking).
- **Nginx Load Balancer (`backend-lb`)**: Distributes traffic between the two Flask backends.

### 3. Celery Workers
- **Workers (`celery_worker1`, `celery_worker2`)**: Perform asynchronous price scraping and updates.

### 4. Frontend
- **Static Servers (`frontend1`, `frontend2`)**: Serve the static HTML/JS front end via Express.js.
- **Nginx Load Balancer (`frontend-lb`)**: Distributes incoming requests across the two frontend servers and proxies API calls.

## Getting Started

### Prerequisites
- **Docker & Docker Compose** installed and running.
  ```bash
  docker --version
  docker-compose --version

git clone https://github.com/your-username/ecommerce-price-tracker.git
cd ecommerce-price-tracker
docker-compose up -d
