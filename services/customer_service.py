from models.customer_model import customers, customers_x_dishes
from utils.lock_manager import lock
from flask import jsonify

def create_customer(data):
    # Extract 'customer_name' from the request data
    customer_name = data.get('customer_name')

    # Check if 'customer_name' is missing or invalid
    if not isinstance(customer_name, str) or customer_name.strip() == "":
        return jsonify({"error": "Customer name cannot be empty"}), 400

    # Reuse the lowest available ID
    available_id = next((i for i in range(len(customers)) if i not in customers), len(customers))
    customers[available_id] = customer_name.strip()

    return jsonify({"message": f"Customer added with ID {available_id}"}), 200

def remove_customer(data):
    print(data)
    customer_id = data.get('customer_id')

    if customer_id is None:
        return jsonify({"error": "Missing required parameters"}), 400

    customer_id = int(customer_id)
    print(customer_id)
    print(customers)

    with lock:
        if customer_id not in customers:
            return jsonify({"error": "No Customer with Id provided"}), 400

        delete_customer(customer_id)
        return jsonify({"message": "Customer removed successfully"}), 200

def delete_customer(customer_id):
    #del customers_x_dishes[customer_id]
    del customers[customer_id]
