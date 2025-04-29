# Use a minimal Python 3.11 image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt ./

# Install Python dependencies without caching to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files into the container's working directory
COPY . .

# Define the command to run the Flask app
CMD ["python", "app.py"]
