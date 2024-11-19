from models.customer_model import customers, customers_x_dishes
from utils.lock_manager import lock
from flask import jsonify

def create_customer(data):
    customer_name = data.get('customer_name')
    if not customer_name:
        return jsonify({"error": "Missing required parameters"}), 400

    with lock:
        if customer_name in customers.values():
            return jsonify({"error": "Customer with the same name already registered"}), 409

        new_customer_id = max(customers.keys(), default=0) + 1
        customers[new_customer_id] = customer_name
        return jsonify({"message": "Customer created successfully"}), 200

def remove_customer(data):
    customer_id = data.get('customer_id')
    if not customer_id:
        return jsonify({"error": "Missing required parameters"}), 400

    with lock:
        if customer_id not in customers:
            return jsonify({"error": "No Customer with Id provided"}), 400

        delete_customer(customer_id)
        return jsonify({"message": "Customer removed successfully"}), 200

def delete_customer(customer_id):
    del customers_x_dishes[customer_id]
    del customers[customer_id]
