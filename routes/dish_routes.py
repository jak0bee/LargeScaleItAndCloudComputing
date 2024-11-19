# routes/dish_routes.py
from flask import Blueprint, request, jsonify
from services.dish_service import order_dish, add_dish, remove_dish, pay_dish

# Create a blueprint for dish-related routes
dish_blueprint = Blueprint('dish', __name__)

@dish_blueprint.route('/order_dish', methods=['POST'])
def order_dish_route():
    data = request.json
    return order_dish(data)

@dish_blueprint.route('/add_dish', methods=['POST'])
def add_dish_route():
    data = request.json
    return add_dish(data)

@dish_blueprint.route('/remove_dish', methods=['POST'])
def remove_dish_route():
    data = request.json
    return remove_dish(data)

@dish_blueprint.route('/pay_dish', methods=['POST'])
def pay_dish_route():
    data = request.json
    return pay_dish(data)
