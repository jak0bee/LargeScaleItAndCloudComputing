from flask import Blueprint, request, jsonify

from services.dish_service import order_dish, add_dish, remove_dish, pay_dish, get_all_dishes
from utils.auth_utils import customer_role_required, kitchen_role_required

dish_blueprint = Blueprint('dish', __name__)

@dish_blueprint.route('/order_dish', methods=['POST'])
@customer_role_required
def order_dish_route():
    """
    Order a Dish
    ---
    tags:
      - Dish Operations
    summary: Place an order for a specific dish.
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            customer_id:
              type: string
              description: The unique identifier of the customer.
              example: "12345"
            dish_id:
              type: string
              description: The unique identifier of the dish.
              example: "67890"
    responses:
      200:
        description: Dish ordered successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Dish ordered successfully!"
      400:
        description: Missing or invalid parameters.
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
@kitchen_role_required
def add_dish_route():
    """
    Add a New Dish
    ---
    tags:
      - Dish Operations
    summary: Add a new dish to the menu. Requires appropriate user permissions.
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            dish_id:
              type: string
              description: The unique identifier of the dish.
              example: "67890"
            price:
              type: number
              description: The price of the dish.
              example: 15.99
    responses:
      200:
        description: Dish added successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Dish added successfully!"
      403:
        description: Permission denied.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "You do not have permission to add a dish"
      400:
        description: Missing or invalid parameters.
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
@kitchen_role_required
def remove_dish_route():
    """
    Remove a Dish
    ---
    tags:
      - Dish Operations
    summary: Remove a dish from the menu.
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            dish_id:
              type: string
              description: The unique identifier of the dish.
              example: "67890"
    responses:
      200:
        description: Dish removed successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Dish removed successfully!"
      400:
        description: Missing or invalid parameters.
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
@customer_role_required
def pay_dish_route():
    """
    Pay for Dishes
    ---
    tags:
      - Dish Operations
    summary: Make a payment for the ordered dishes.
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            customer_id:
              type: string
              description: The unique identifier of the customer.
              example: "12345"
            total_price:
              type: number
              description: The total price of the ordered dishes.
              example: 45.50
    responses:
      200:
        description: Payment successful.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Payment successful!"
      400:
        description: Missing or invalid parameters.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Missing required parameters"
    """
    data = request.json
    return pay_dish(data)

@dish_blueprint.route('/get_all_dishes', methods=['GET'])
def get_all_dishes_route():
    """
    Get All Dishes
    ---
    tags:
      - Dish Menu
    responses:
      200:
        description: List of all dishes
        schema:
          type: array
          items:
            type: object
            properties:
              dish_id:
                type: string
                example: "dish1"
              available:
                type: boolean
                example: true
              price:
                type: number
                example: 12.99
    """
    return get_all_dishes()  # Call the function directly, no need to wrap with jsonify

