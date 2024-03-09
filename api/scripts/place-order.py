import requests
import json
from datetime import datetime, timedelta
import random
import time

# Define the base URL for the place-order endpoint
base_url = 'http://127.0.0.1:8000/api/place-order/script/'

# Counter to track the orders being placed
counter = 1

# Generate 1000 dummy orders
for _ in range(1000):
    # Generate random dummy data for the order
    user_id = random.randint(1, 1008)
    shipping_address = ' '.join([str(random.randint(1, 1000)), 'Main St'])
    ordered_items = []

    # Generate random number of ordered items
    num_items = random.randint(1, 5)
    for _ in range(num_items):
        item = {
            'product_id': random.randint(1, 1000),
            'quantity': random.randint(1, 10),
            'size': random.choice(['XS', 'S', 'M', 'L', 'XL']),
            'color': random.choice(['Red', 'Blue', 'Green', 'Yellow', 'Black'])
        }
        ordered_items.append(item)

    # Prepare data for the request
    order_data = {
        'user_id': user_id,
        'shipping_address': shipping_address,
        'ordered_items': ordered_items
    }

    # Send a POST request with dummy data
    response = requests.post(base_url, data=json.dumps(order_data))

    # Check if the request was successful
    if response.status_code == 201:
        print(f'Order {counter} placed successfully for user {user_id}')
    else:
        print(f'Failed to place order {counter} for user {user_id}')

    # Increment the counter
    counter += 1

    # Add a delay of 0.05 seconds
    time.sleep(0.05)
