from models.dish_model import dishes
from models.customer_model import customers_x_dishes
from utils.lock_manager import lock
from flask import jsonify

# Order a dish for a customer
def order_dish(data):
    customer_id = data.get('customer_id')
    dish_id = data.get('dish_id')

    if not customer_id or not dish_id:
        return jsonify({"error": "Missing required parameters"}), 400

    with lock:
        if customer_id not in customers_x_dishes:
            return jsonify({"error": "No customer with provided id"}), 400
        if dish_id not in dishes:
            return jsonify({"error": "No dish with provided id"}), 400
        if not dishes[dish_id][0]:  # Check if dish is available
            return jsonify({"error": "Dish not available"}), 400

        # Add the dish to the customer's order list
        order_list = customers_x_dishes.get(customer_id, [])
        order_list.append(dish_id)
        customers_x_dishes[customer_id] = order_list

        return jsonify({"message": "Dish ordered successfully"}), 200

# Add a new dish to the menu
def add_dish(data):
    dish_id = data.get("dish_id")
    price = data.get("price")

    if not dish_id or price is None:
        return jsonify({"error": "Missing required parameters"}), 400

    with lock:
        if dish_id in dishes:
            return jsonify({"error": "Dish with that id already exists"}), 400
        if price <= 0:
            return jsonify({"error": "Price must be positive"}), 400

        # Add the dish with availability set to True
        dishes[dish_id] = [True, price]
        return jsonify({"message": "Dish added successfully"}), 200

# Remove a dish from the menu
def remove_dish(data):
    dish_id = data.get('dish_id')

    if not dish_id:
        return jsonify({"error": "Missing required parameters"}), 400

    with lock:
        if dish_id not in dishes:
            return jsonify({"error": "No dish with provided id"}), 400

        # Remove the dish from the menu
        del dishes[dish_id]
        return jsonify({"message": "Dish removed successfully"}), 200

# Pay for a customer's ordered dishes
def pay_dish(data):
    customer_id = data.get('customer_id')

    if not customer_id:
        return jsonify({"error": "Missing required parameters"}), 400

    with lock:
        if customer_id not in customers_x_dishes or not customers_x_dishes[customer_id]:
            return jsonify({"error": "No orders found for this customer"}), 400

        total_price = 0
        # Calculate the total price of all ordered dishes
        for dish_id in customers_x_dishes[customer_id]:
            if dish_id in dishes:
                total_price += dishes[dish_id][1]  # Add the price of the dish

        # Clear the customer's orders after payment
        customers_x_dishes[customer_id] = []

        return jsonify({"message": "Payment successful", "total_price": total_price}), 200


def get_all_dishes():
    """
    Returns a list of all dishes with their availability and price.
    """
    with lock:
        all_dishes = []
        for dish_id, (available, price) in dishes.items():
            all_dishes.append({
                "dish_id": dish_id,
                "available": available,
                "price": price
            })
        return jsonify(all_dishes), 200