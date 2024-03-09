import time
import requests
from faker import Faker
import random
from datetime import datetime

# Initialize Faker to generate dummy data
fake = Faker()

# Define the URL for the add-product endpoint
url = 'http://127.0.0.1:8000/api/add-product/script/'

# Counter to track the products being added
counter = 1

# Generate 1000 dummy entries
for _ in range(1000):
    # Generate random dummy data
    dummy_data = {
        'name': fake.word(),  # Random word for product name
        'description': fake.text(),  # Random text for description
        # Random price between 1 and 1000
        'price': round(random.uniform(1, 1000), 2),
        # Random quantity between 1 and 100
        'quantity': random.randint(1, 100),
        'category': fake.word(),  # Random word for category
        # Random boolean value
        'multiple_products': random.choice([True, False]),
        'used': random.choice([True, False]),  # Random boolean value
        # Random owner ID from 1 to 1008
        'owner_id': random.randint(1, 1008),
        # Add other fields as needed
    }

    # Send a POST request with dummy data
    response = requests.post(url, data=dummy_data, 
                             )

    # Check if the request was successful
    if response.status_code == 201:
        print(f'Product {counter} added successfully')
    else:
        print(f'Failed to add product {counter}')

    # Increment the counter
    counter += 1

    # You might want to add some delay between requests to avoid overwhelming the server
    time.sleep(0.05)  # Uncomment this line if needed
