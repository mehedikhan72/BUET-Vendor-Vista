import requests
import json
from datetime import datetime, timedelta
import random
import time

# Define the base URL for the add-product-size endpoint
base_url = 'http://127.0.0.1:8000/api/add-product-size/'

# Counter to track the sizes being added
counter = 1

# Generate 1000 dummy sizes
for _ in range(1000):
    # Generate random dummy data for size
    product_id = random.randint(1, 1000)
    size = random.choice(['XS', 'S', 'M', 'L', 'XL'])
    quantity = random.randint(1, 100)

    # Prepare data for the request
    size_data = {
        'size': size,
        'quantity': quantity
    }

    # Send a POST request with dummy data
    response = requests.post(f'{base_url}{product_id}/script/', data=size_data)

    # Check if the request was successful
    if response.status_code == 201:
        print(f'Size {size} added successfully for product {product_id}')
    else:
        print(f'Failed to add size {size} for product {product_id}')

    # Increment the counter
    counter += 1

    # Add a delay of 0.05 seconds
    time.sleep(0.05)
