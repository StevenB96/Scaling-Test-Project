// Import the required modules: express for the server and path for handling file paths
const express = require('express');
const path = require('path');

// Create an Express application instance
const app = express();

// Serve static files (like HTML, CSS, JS) from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Set the application to listen on port 80 (default HTTP port) and log a message when the server starts
app.listen(80, () => {
  console.log('Frontend server running on port 80');
});
