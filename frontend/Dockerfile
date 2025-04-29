# Use the official Node.js 18 image as the base image for the container
FROM node:18

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the package.json file into the working directory in the container
COPY package.json ./

# Install the Node.js dependencies listed in package.json
RUN npm install

# Copy all the remaining files (including app.js, public directory, etc.) into the container's /app directory
COPY . .

# Define the command to start the application when the container runs
CMD ["npm", "start"]
