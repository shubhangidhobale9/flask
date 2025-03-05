import requests
import json

API_URL = "http://192.168.48.39:5000/api/data"  # Use your actual IP

# Simulating large data
large_data = [{"id": i, "name": f"Product {i}", "price": i * 10.5} for i in range(1, 10001)]  # 10,000 items

CHUNK_SIZE = 1000  # Send 1000 items per request

for i in range(0, len(large_data), CHUNK_SIZE):
    chunk = large_data[i:i + CHUNK_SIZE]  # Slice data
    response = requests.post(API_URL, json=chunk, timeout=60)  # Send chunk
    print(f"Sent {len(chunk)} records - Status: {response.status_code}")

print("✅ Data upload complete!")


