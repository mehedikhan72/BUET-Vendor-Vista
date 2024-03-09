import requests
from faker import Faker
import random
import time

# Define the base URL for the add-product-color endpoint
base_url = 'http://127.0.0.1:8000/api/add-product-color/'

# Counter to track the products being added
counter = 1

# Generate 1000 dummy entries
for _ in range(1000):
    # Generate random dummy data
    product_id = random.randint(1, 1008)
    color = Faker().color_name()
    quantity = random.randint(1, 100)

    # Send a POST request with dummy data
    response = requests.post(f'{base_url}{product_id}/script/', data={'color': color, 'quantity': quantity})

    # Check if the request was successful
    if response.status_code == 201:
        print(f'Color added successfully for product {product_id}')
    else:
        print(f'Failed to add color for product {product_id}')

    # Increment the counter
    counter += 1

    # Add a delay of 0.05 seconds
    time.sleep(0.05)
