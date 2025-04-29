import random

def fetch_price(url):
    # Simulate scraping the product price from a given URL
    # In a real implementation, this function would make an HTTP request to the URL and parse the price
    return round(random.uniform(10.0, 100.0), 2)  # Return a random price between $10.00 and $100.00 (rounded to 2 decimal places)
