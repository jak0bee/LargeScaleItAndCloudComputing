from models.kitchen_model import orders_queue
# from models.customer_model import customers_x_dishes
from utils.lock_manager import lock
from flask import jsonify
from database.database_connection import app, db
from sqlalchemy.exc import SQLAlchemyError

# Order a dish for a customer
def order_dish(data):
    customer_id = data.get('customer_id')
    dish_id = data.get('dish_id')

    if customer_id is None or dish_id is None:
        dev_log('Tried ordering a dish with missing parameters')
        return jsonify({"error": "Missing required parameters"}), 400

    customer_id = int(customer_id)

    with lock:
        if check_customer_id(customer_id) == 0:
            dev_log('Invalid customerId provided')
            return jsonify({"error": "No customer with provided id"}), 400

        dish_check_result = check_dish_availability(int(dish_id))
        if dish_check_result == -1:
            dev_log('Invalid dishId provided')
            return jsonify({"error": "No dish with provided id"}), 400

        if dish_check_result == 0:  # Check if dish is available
            dev_log(f'Dish not available for customerId={customer_id}, dishId={dish_id}')
            return jsonify({"error": "Dish not available"}), 400

        # Add the dish to the list of orders to be prepared
        new_order = {dish_id: customer_id}
        orders_queue.append(new_order)

        # Decrease the availability of the dish
        try:
            if decrease_dish_availability(dish_id) == 1:
                dev_log(f'Dish ordered successfully: customerId={customer_id}, dishId={dish_id}')
                return jsonify({"message": "Dish ordered successfully"}), 200
            else:
                dev_log(f'Error while decreasing dish availability: customerId={customer_id}, dishId={dish_id}')
                return jsonify({"error": "Error while decreasing the dish availability. Please contact the administrator"}), 500
        except Exception as e:
            dev_log(f'Exception while decreasing dish availability: {e}')
            return jsonify({"error": "An unexpected error occurred"}), 500


# Add a new dish to the menu
def add_dish(data):
    name = data.get("name")
    description = data.get('description')
    ammount_available = int(data.get('ammount_available'))
    price = float(data.get("price"))
    
    with lock:

        if not price or not name or not description or not ammount_available:
            dev_log('Tried adding a dish without needed parameters')
            return jsonify({"error": "Missing required parameters"}), 400

        if not isinstance(price, float):
            dev_log('Tried adding a dish with price not a float')
            return jsonify({"error": "price parameter needs to be a float"}), 400
        
        if not isinstance(ammount_available,int):
            dev_log('Tried adding a dish with ammount_avaialble not an int')
            return jsonify({"error": "ammount_available parameter needs to be an int"}), 400

        if not isinstance(name,str):
            dev_log('Tried adding a dish with name not a string')
            return jsonify({"error": "name parameter needs to be a string"}), 400
        
        if not isinstance(description,str):
            dev_log('Tried adding a dish with description not a string')
            return jsonify({"error": "description parameter needs to be a string"}), 400
        
        if price < 0:
            dev_log('Tried adding a dish with negative price')
            return jsonify({"error": "price parameter needs to be not negative"}), 400

        result = insert_dish(name, description, ammount_available, price)
        if result >= 1:
            return jsonify({"message": "Dish added successfully"}), 200
        else:
            dev_log('Error while inserting a dish')
            return jsonify({"error": "error while inserting a dish, contact an administrator"}), 400

# Remove a dish from the menu, mode = 1 delete if its not in any orders (payed or not), mode =2 delte and delete from orders
def remove_dish(data):
    dish_id = int(data.get('dish_id'))
    mode = int(data.get('mode'))

    if not dish_id or not mode:
        dev_log('Tried removing a dish with missing parameters')
        return jsonify({"error": "Missing required parameters"}), 400

    with lock:
        if not isinstance(mode,int):
            dev_log('tried removing a dish with mode that is not a string')
            return jsonify({"error": "mode parameter has to be an int with value 1 or 2"}), 400

        if mode not in [1,2]:
            dev_log('tried removing a dish with mode that is not 1 or 2')
            return jsonify({"error": "mode parameter has to be an int with value 1 or 2"}), 400

        if not isinstance(dish_id,int):
            dev_log('tried removing a dish with dishId parameter that is not an int')
            return jsonify({"error": "dishId parameter has to be an int"}), 400
    
        dish_availability_result =  check_dish_availability(dish_id)
    
        if dish_availability_result == -1:
            dev_log('tried deleting a dish with a wrong Id')
            return jsonify({"error": "No dish with provided id"}), 400

        if mode == 1:
            if check_dish_removal != 0:
                dev_log('tried removing a dish while it was in some orders')
                return jsonify({"error": "dish cant be removed in mode 1 while in orders"}), 400
            else:
                hard_remove_dish(dish_id)
                return jsonify({"message": "Dish removed successfully"}), 200
            
        if mode == 2:
            hard_remove_dish(dish_id)
            return jsonify({"message": "Dish removed successfully"}), 200


# Pay for a customer's ordered dishes
def pay_orders(data):
    customer_id = data.get('customer_id')

    if customer_id is None:  # Check for missing parameter
        dev_log('tried paying for order with data missing a customerId')
        return jsonify({"error": "Missing required parameters"}), 400

    with lock:
        if not isinstance(customer_id, int):
            dev_log('tried paying for order with customerId not being an int')
            return jsonify({"error": "customer_id parameter has to be an int"}), 400

        total_price = check_price_total(customer_id)

        # Clear the customer's orders after payment
        pay_customers_orders(customer_id)
        dev_log('customer ' + str(customer_id) + ' payed ' + str(total_price) + ' for all his orders')
        return jsonify({"message": "Payment successful", "total_price": total_price}), 200


def get_all_dishes():
    """
    Returns a list of all dishes with their availability and price.
    """
    try:
        with app.app_context():
            query = db.text("""
                SELECT Id AS dish_id, ammountAvaialable AS available, price
                FROM Dishes
            """)
            result = db.session.execute(query).fetchall()

            all_dishes = [
                {
                    "dish_id": row.dish_id,
                    "available": row.available,
                    "price": row.price
                }  
                for row in result
            ]

            return jsonify(all_dishes), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Failed to fetch dishes", "details": str(e)}), 500


def get_all_customers_dishes():
    """
    Returns a list of all customers with their received dishes.
    """
    try:
        with app.app_context():
            # Query the Customers and their dishes
            query = db.text("""
                SELECT
                    c.Id AS customer_id,
                    COALESCE(
                        CONCAT('[', GROUP_CONCAT(
                            DISTINCT JSON_OBJECT('dish_id', d.Id, 'name', d.name)
                            SEPARATOR ', '
                        ), ']'), '[]') AS dishes
                FROM Customers c
                LEFT JOIN Orders o ON c.Id = o.CustomerId
                LEFT JOIN OrderXdish od ON o.Id = od.OrderId
                LEFT JOIN Dishes d ON od.DishId = d.Id
                GROUP BY c.Id;
            """)
            result = db.session.execute(query).fetchall()

            # Transform result into a list of dictionaries
            all_customers_dishes = [
                {
                    "customer_id": row.customer_id,
                    "dishes": row.dishes
                }
                for row in result
            ]

            return jsonify(all_customers_dishes), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Failed to fetch customer dishes", "details": str(e)}), 500



def prepare_next_dish():
    """
    Prepares the next dish in the orders queue (here instantly). This should be called any time a kitchen / cook is free
    """
    with lock:
        if not orders_queue:
            dev_log('tried to prepare orders with nothing in the queue')
            return jsonify({"error": "No orders to prepare"}), 400

        # Get the first order in the queue
        order = orders_queue.pop(0)
        dish_id, customer_id = order.popitem()

        # Check to what order should we add the dish
        orderId = get_latest_order(customer_id)
        add_dish_to_order(dish_id, orderId)

        # No need to decrease availability, because it will be decresed upon ordering -
        message = f"Dish {dish_id} prepared for customer {customer_id}"
        dev_log(message)
        return jsonify({"message": f"Dish {dish_id} prepared for customer {customer_id}"}), 200
    


## METHODS TO INTERACT WITH THE DATABASE


def check_dish_availability(dish_id):
    if isinstance(dish_id, str):
        dish_id = int(dish_id)
    if not isinstance(dish_id, int):
        dish_id = dish_id.get('dish_id')
    

    result = ''
    with app.app_context():
        query = db.text("""
    SELECT ammountAvaialable FROM Dishes WHERE Id = 
    """ + str(dish_id))
        result = db.session.execute(query)
        result_int = result.scalar()

    if result_int is None:
        return -1
    
    return result_int
    

def dev_log(event):
    # ONLY FOR CONTROLLED USE WITH PRE SET MESSAGES PRONE TO SQL INJECTION
    with app.app_context():
        query = db.text("INSERT INTO Log(TimeStamp, Event) VALUES(NOW(), '" + str(event) + """')""")
        result = db.session.execute(query)
        db.session.commit()


def check_customer_id(customer_id):
    result = ''
    with app.app_context():
        query = db.text("""
    SELECT COUNT(Id) FROM Customers WHERE Id = 
    """ + str(customer_id))
        result = db.session.execute(query)
        result_int = result.scalar()

    return result_int

def decrease_dish_availability(dish_id:int):
    with app.app_context():
        current_ammount = check_dish_availability(dish_id)
        if current_ammount == -1:
            dev_log('tried decreasing a dish with wrong dishId')
            return -1
        if current_ammount == 0:
            dev_log('tried decreasing a dish that was not available, dishId = ' + str(dish_id))
            return -1
        query = db.text("""UPDATE Dishes SET ammountAvaialable =  """ + str(current_ammount - 1))

        result = db.session.execute(query)
        db.session.commit()

        return 1
    
def insert_dish(name: str, description: str, ammount_available: int, price: float):
    with app.app_context():
        query = db.text("""
            INSERT INTO Dishes (name, description, ammountAvaialable, price)
            VALUES (:name, :description, :ammountAvaialable, :price)
        """)
        result = db.session.execute(
            query,
            {
                "name": name,
                "description": description,
                "ammountAvaialable": ammount_available,
                "price": price
            }
        )
        db.session.commit()

        # Return the ID of the newly inserted dish if available
        return result.lastrowid if hasattr(result, "lastrowid") else "Insert successful"


def check_dish_removal(dish_id : int):
    result = ''
    with app.app_context():
        query = db.text("""
            SELECT COUNT(Id) FROM OrderXdish WHERE DishId = :dish_id
        """)
        result = db.session.execute(
        query,
        {
            "dish_id": str(dish_id)
        }
        )
        result = result.scalar()

    return result

def hard_remove_dish(dish_id : int):
    with app.app_context():
        query = db.text("""
            CALL hardDeleteDish(:dishId)
        """)
        result = db.session.execute(
            query,
            {
                "dishId": dish_id
            }
        )
        db.session.commit()
    return 1

def check_price_total(customer_id):
    result = ''
    with app.app_context():
        query = db.text("""
            CALL getCustomersTotal(:customer_id)
        """)
        result = db.session.execute(
        query,
        {
            "customer_id": str(customer_id)
        }
        )
        result = result.scalar()
    return result


def pay_customers_orders(customer_id):
    with app.app_context():
        query = db.text("""
            UPDATE Orders Set isPayed = 1 WHERE CustomerId = :customerId
        """)
        result = db.session.execute(
            query,
            {
                "customerId": customer_id
            }
        )
        db.session.commit()
    return 1

def get_latest_order(customer_id):
    with app.app_context():
        query = db.text("""
            SELECT Id FROM Orders WHERE CustomerId = :customerId AND isPayed = 0 ORDER BY ID LIMIT 1;
        """)
        result = db.session.execute(
            query,
            {
                "customerId": customer_id
            }
        )
        result = result.scalar()
    return result

def add_dish_to_order(dish_id, order_id):
    with app.app_context():
        query = db.text("""
            INSERT INTO OrderXdish(OrderId, DishId)
            VALUES(:orderId, :dishId)
        """)
        result = db.session.execute(
            query,
            {
                "orderId": order_id,
                "dishId": dish_id
            }
        )
        db.session.commit()
    return 1