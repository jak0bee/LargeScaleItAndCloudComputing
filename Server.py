from flask import Flask, request, jsonify
import threading
import bcrypt

app = Flask(__name__)

customers = {
    # customerId : [orderId, orderId]
}
orders = {
    # orderId : [dishId, dishId]
}
dishes = {
    # dishId : price
}

lock = threading.Lock() 

@app.route('/create_customer', methods=['POST'])
def create_customer():
    data = request.json
    customer_id = data.get('id')

    # Check the required data
    if not all([customer_id]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Check if the customer_id is in the data, else return the error
    customers[customer_id] = []

@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.json
    customer_id = data.get('id')
    # Check the required data
    if not all([customer_id]):
        return jsonify({"error": "Missing required parameters"}), 400
    
    # Check if the customerId is correct
    if customer_id not in customers:
        return jsonify({"error": "Missing required parameters"}), 400


@app.route('/add_dish', methods=['POST'])
def add_dish():
    data = request.json
    order_id = data.get('order_id')
    dish_id = data.get('dish_id')

    if order_id not in orders:
        pass
        # Return the error for incorrect OrderId

    if dish_id in dishes:
        orders[order_id].add(dish_id)
    else:
        pass
        # return the error for invalid dish    




@app.route('/remove_dish', methods=['POST'])
def remove_dish():
    data = request.json
    order_id = data.get('order_id')
    dish_id = data.get('dish_id')
