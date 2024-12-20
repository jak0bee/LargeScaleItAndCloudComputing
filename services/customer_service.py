# from models.customer_model import customers, customers_x_dishes
from utils.lock_manager import lock
from flask import jsonify

def create_customer(data):
    # Extract 'customer_name' from the request data
    customer_name = data.get('customer_name')

    # Check if 'customer_name' is missing or invalid
    if not isinstance(customer_name, str) or customer_name.strip() == "":
        return jsonify({"error": "Customer name cannot be empty"}), 400

    # Reuse the lowest available ID
    insert_customer(name= customer_name)

    return jsonify({"message": f"Customer added with ID {available_id}"}), 200



def remove_customer(data):
    customer_id = data.get('customer_id')
    if customer_id is None:
        return jsonify({"error": "Missing required parameters"}), 400

    customer_id = int(customer_id)

    with lock:
        hard_remove_customer(customer_id)
        return jsonify({"message": "Customer removed successfully"}), 200

## Methods for interacting with the database
    
def insert_customer(name : str):
    with app.app_context():
        query = db.text("""
            INSERT INTO Customer (name)
            VALUES (:name)
        """)
        result = db.session.execute(
            query,
            {
                "name": name
            }
        )
        db.session.commit()
    return 1



def hard_remove_customer(customer_id : int):
    with app.app_context():
        query = db.text("""
            CALL hardDeleteCustomer(:customerId)
        """)
        result = db.session.execute(
            query,
            {
                "customerId": customer_id
            }
        )
        db.session.commit()
    return 