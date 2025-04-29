// Function to load and display the list of products from the backend
async function loadProducts() {
  // Fetch the list of products from the server's "/products" endpoint
  const res = await fetch('/products');

  // Parse the response as JSON to get the product data
  const products = await res.json();

  // Get the <ul> element where the products will be displayed
  const list = document.getElementById('products');

  // Loop through each product and create a new <li> for each one
  products.forEach(p => {
    const li = document.createElement('li'); // Create a new list item
    li.textContent = `${p.name}: $${p.price}`;  // Set the text to display product name and price
    list.appendChild(li); // Append the <li> to the <ul> in the DOM
  });
}

// Function to trigger a price check by sending a POST request to the backend
async function triggerCheck() {
  // Send a POST request to the "/check" endpoint to initiate the price check
  const res = await fetch('/check', { method: 'POST' });

  // Parse the response and extract the message to show in an alert
  const { message } = await res.json();

  // Show an alert with the response message (e.g., "Price check triggered")
  alert(message);
}

// Load the list of products when the page is loaded
window.onload = loadProducts;
