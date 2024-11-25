from flask import Blueprint, request, jsonify
from services.dish_service import order_dish, add_dish, remove_dish, pay_dish

dish_blueprint = Blueprint('dish', __name__)

@dish_blueprint.route('/order_dish', methods=['POST'])
def order_dish_route():
    """
    Ordering a dish
    ---
    tags:
      - Ordering a dish
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            customer_id:
              type: string
              description: The unique identifier of the customer
              example: "12345"
            dish_id:
              type: string
              description: The unique identifier of the dish
              example: "67890"
    responses:
      200:
        description: Success
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Dish ordered successfully!"
      400:
        description: Failure
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Missing required parameters"
    """
    data = request.json
    return order_dish(data)

@dish_blueprint.route('/add_dish', methods=['POST'])
def add_dish_route():
    """
    Adding a dish
    ---
    tags:
      - Adding a dish
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            dish_id:
              type: string
              description: The unique identifier of the dish
              example: "67890"
            price:
              type: number
              description: Price of the dish
              example: 15.99
    responses:
      200:
        description: Success
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Dish added successfully!"
      400:
        description: Failure
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Missing required parameters"
    """
    data = request.json
    return add_dish(data)

@dish_blueprint.route('/remove_dish', methods=['POST'])
def remove_dish_route():
    """
    Removing a dish
    ---
    tags:
      - Removing a dish
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            dish_id:
              type: string
              description: The unique identifier of the dish
              example: "67890"
    responses:
      200:
        description: Success
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Dish removed successfully!"
      400:
        description: Failure
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Missing required parameters"
    """
    data = request.json
    return remove_dish(data)

@dish_blueprint.route('/pay_dish', methods=['POST'])
def pay_dish_route():
    """
    Paying for a dish
    ---
    tags:
      - Paying for a dish
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            customer_id:
              type: string
              description: The unique identifier of the customer
              example: "12345"
            total_price:
              type: number
              description: Total price of the dishes
              example: 45.50
    responses:
      200:
        description: Success
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Payment successful!"
      400:
        description: Failure
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Missing required parameters"
    """
    data = request.json
    return pay_dish(data)
