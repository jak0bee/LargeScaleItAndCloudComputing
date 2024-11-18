import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

customers = {
    # customer_id : customer_name
}
customers_x_dishes = {
    # customerId : [orderId, orderId]
}

dishes = {
    # dishId : [isAvailable, price]
}

lock = threading.Lock() 

@app.route('/create_customer', methods=['POST'])
def create_customer():
    data = request.json
    customer_name = data.get('customer_name')

    # Check the required data
    # TODO: check if the name is a string
    if not all([customer_name]):
        return jsonify({"error": "Missing required parameters"}), 400

    with lock:
        # Check if the customer is already there, if it is -> return an error
        if customer_name in customers.values:
            return jsonify({"error": "Customer with the same name already registered"},409)

        # If its not, add the customer
        mew_customer_id = max(customers.keys(), default=0) + 1
        customers[mew_customer_id] = customer_name
        return jsonify({"message": "Customer created successfully"}, 200)
    
    return jsonify({"error": "Unexpected error"},400)


@app.route('/remove_customer', methods=['POST'])
def remove_customer():
    data = request.json
    customer_id = data.get('customer_id')
    # TODO: check if the customerId is an int
    # Check the required data
    if not all([customer_id]):
        return jsonify({"error": "Missing required parameters"}), 400
    with lock:
        # Check if the customerId is in use, if its not -> return an error
        if customer_id not in customers:
            return jsonify({"error": "No Customer with Id provided"},400)
        
        # Delete the customer and their data
        delete_customer(customer_id)
        return jsonify({"message": "Customer removed successfully"}), 200

    return jsonify({"error": "Unexpected error"},400)

# TODO: add an endpoint to check dish availability

# Question: Should it take only one dish or an array of dishes (id-s)
@app.route('/order_dish', methods=['POST'])
def order_dish():
    data = request.json
    customer_id = data.get('customer_id')
    dish_id = data.get('dish_id')

    # Check the required data
    if not all([customer_id]):
        return jsonify({"error": "Missing required parameters"}), 400
    
    with lock:
        # Check if the customerId and dishId is correct
        if customer_id not in customers:
            return jsonify({"error": "No customer with provided id"}), 400    
        if dish_id not in dishes:
            return jsonify({"error": "No dish with provided id"}), 400    
        # Check if the dish is available
        if dishes[dish_id][0] == False:
            return jsonify({"error": "Dish not available"}), 400    
        
        # Add the dish to the customer's order
        customers_x_dishes[customer_id] = customers_x_dishes.get(customer_id, []).add(dish_id) 
    
        return jsonify({"message": "Dish ordered successfully"}), 200

    return jsonify({"error": "Unexpected error"},400)



# TODO: Finish
@app.route('/add_dish', methods=['POST'])
def add_dish():
    data = request.json
    dish_id = data.get("dish_id")
    #dish_name = data.get("dish_name")
    #ingredients = data.get("ingredients")
    price = data.get("price")
    with lock:
        # Check if the dishId already exists
        if dish_id in dishes:
            return jsonify({"error": "Dish with that id already exists"}), 400   
        # Check if price is posiitve 
        if price <=0:
            return jsonify({"error": "Price has to be positive"}), 400    
        
        # Add the dish to the dishes
        new_dish_id = max(dishes.keys(), default=0) + 1

        dishes[new_dish_id] = [True, price]

        return jsonify({"message": "Dish added successfully"}), 200

    return jsonify({"error": "Unexpected error"},400)


# TODO: Finish
@app.route('/remove_dish', methods=['POST'])
def remove_dish():
    data = request.json
    order_id = data.get('order_id')
    dish_id = data.get('dish_id')


def delete_customer(customer_id):
    # Remove the customer's orders
    del customers_x_orders[customer_id]
    # Remove the customer
    del customers[customer_id]

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)