# E-commerce Price Tracker (Sharded + Load Balanced)

## Overview
This stack implements a price-tracking application that tracks product prices from e-commerce websites. The application is designed for scalability and fault tolerance using the following components:

- **Sharded MongoDB Cluster**: A MongoDB cluster with two shards, a config server, and a mongos router for horizontal scaling.
- **Flask API**: The backend REST API for managing products and triggering price checks. It’s replicated behind an Nginx load balancer for high availability.
- **Celery Workers**: Two Celery worker services that scrape product prices asynchronously.
- **Frontend**: A dynamic web application built with **Express.js**, served by two replicas behind an Nginx load balancer.

## Components

### 1. **MongoDB Sharded Cluster**
   - **Config Server (`configsvr`)**: Stores configuration and metadata for the sharded MongoDB cluster.
   - **Shards (`shard1` and `shard2`)**: Each shard holds a subset of the data.
   - **Mongos Router**: A routing service that directs client requests to the appropriate shard.

### 2. **Flask Backend API**
   - **Backend Services (`backend` and `backend2`)**: Handle product-related requests (e.g., viewing, tracking).
   - **Nginx Load Balancer (`api-lb`)**: Balances traffic between the two backend services for load distribution and fault tolerance.

### 3. **Celery Workers**
   - **Celery Worker Services (`celery_worker1` and `celery_worker2`)**: Asynchronously scrape product prices from e-commerce sites and update the MongoDB database.

### 4. **Frontend**
   - **Frontend Services (`frontend1` and `frontend2`)**: Serve the static front-end application (React or similar) to display product prices.
   - **Nginx Frontend Load Balancer (`frontend-lb`)**: Distributes incoming requests across the two frontend containers.

## Getting Started

### Prerequisites
Before running the application, ensure that you have the following installed:

- **Docker**: Ensure that Docker and Docker Compose are installed and running on your machine. 
  - You can download Docker here: https://www.docker.com/products/docker-desktop
  - You can check the installation by running `docker --version` and `docker-compose --version`.

### 1. **Clone the Repository**
   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/ecommerce-price-tracker.git
   cd ecommerce-price-tracker
