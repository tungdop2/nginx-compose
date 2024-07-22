from flask import Flask, request, jsonify
import os
import json
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure the output directory exists
output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

# Get the replica index from the balancer service
balancer_service_url = os.getenv('BALANCER_SERVICE_URL', 'http://balancer:1111')
response = requests.get(balancer_service_url)
replica_index = response.text

# Log the replica index
logger.info(f"Replica Index: {replica_index}")

# In-memory index counter
index = 0

@app.route('/', methods=['POST'])
def create_item():
    global index
    index += 1
    item = request.json
    item['id'] = f"{replica_index}_{index}"

    # Save the item to a file in the output directory
    output_path = os.path.join(output_dir, f"{item['id']}.json")
    with open(output_path, 'w') as f:
        json.dump(item, f)

    # Log the creation of a new item
    logger.info(f"Created item: {item['id']}")

    return jsonify(item), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
