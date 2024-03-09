import time
import requests
from faker import Faker
import random

# Initialize Faker to generate dummy data
fake = Faker()

# Define the URL for the register endpoint
url = 'http://127.0.0.1:8000/api/register/'

# Generate 1000 dummy users
for _ in range(1000):
    # Generate random dummy data
    dummy_data = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        # Random password length between 8 and 16 characters
        'password': fake.password(length=random.randint(8, 16)),
        # Add other fields as needed
    }

    # Send a POST request to register the user
    response = requests.post(url, data=dummy_data)

    # Check if the request was successful
    if response.status_code == 201:
        print('User registered successfully')
    else:
        print('Failed to register user')

    # You might want to add some delay between requests to avoid overwhelming the server
    time.sleep(0.1)  # Uncomment this line if needed
