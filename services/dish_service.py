from models.kitchen_model import dishes, orders
from models.customer_model import customers_x_dishes
from models.customer_model import customers
#from models.customer_model import orders
from utils.lock_manager import lock
from flask import jsonify

# Order a dish for a customer
def order_dish(data):
    customer_id = data.get('customer_id')
    dish_id = data.get('dish_id')

    if customer_id is None or dish_id is None:
        return jsonify({"error": "Missing required parameters"}), 400

    customer_id = int(customer_id)

    with lock:
        if customer_id not in customers:
            print(customers)
            return jsonify({"error": "No customer with provided id"}), 400
        if dish_id not in dishes:
            return jsonify({"error": "No dish with provided id"}), 400
        if dishes[dish_id][0] <= 0:  # Check if dish is available
            return jsonify({"error": "Dish not available"}), 400

        # Add the dish to the list of orders to be prepared
        new_order = {dish_id: customer_id}
        orders.append(new_order)
        dishes[dish_id][0] -= 1  # Decrease the availability of the dish

        return jsonify({"message": "Dish ordered successfully"}), 200

# Add a new dish to the menu
def add_dish(data):
    dish_id = data.get("dish_id")
    price = data.get("price")

    if not dish_id or price is None:
        return jsonify({"error": "Missing required parameters"}), 400

    with lock:
        if dish_id in dishes:
            if price <= 0:
                return jsonify({"error": "Price must be positive"}), 400
            dishes[dish_id][0] += 1  # Increment availability
            return jsonify({"message": "Dish availability increased"}), 200
        if price <= 0:
            return jsonify({"error": "Price must be positive"}), 400

        # Add the dish with availability set to 1
        dishes[dish_id] = [1, price]
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

    if customer_id is None:  # Check for missing parameter
        return jsonify({"error": "Missing required parameters"}), 400

    customer_id = int(customer_id)  # Ensure it's an integer

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



def check_dish_availability(data):
    dish_id = data.get('dish_id')

    if not dish_id:
        return jsonify({"error": "Missing required parameters"}), 400

    with lock:
        if dish_id not in dishes:
            return jsonify({"error": "No dish with provided id"}), 400

        amount_available = int(dishes[dish_id][0])
        price = dishes[dish_id][1]
        message = f"There are {amount_available} dishes available at a price of {price}"

        return jsonify({"message": message}), 200


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

def get_all_customers_dishes():
    """
    Returns a list of all customers with their received dishes.
    """
    with lock:
        all_customers_dishes = []
        for customer_id, dishes_list in customers_x_dishes.items():
            all_customers_dishes.append({
                "customer_id": customer_id,
                "dishes": dishes_list
            })
        return jsonify(all_customers_dishes), 200


def prepare_next_dish():
    """
    Prepares the next dish in the orders queue (here instantly). This should be called any time a kitchen / cook is free
    """
    with lock:
        if not orders:
            return jsonify({"error": "No orders to prepare"}), 400

        # Get the first order in the queue
        order = orders.pop(0)
        dish_id, customer_id = order.popitem()

        # Add the dish to the  customer's bill
        customer_bill = customers_x_dishes.get(customer_id, [])
        customer_bill.append(dish_id)
        customers_x_dishes[customer_id] = customer_bill

        # No need to decrease availability, because it will be decresed upon ordering -
        # Prohibits ordering a dish that will become unavailable later

        return jsonify({"message": f"Dish {dish_id} prepared for customer {customer_id}"}), 200
    