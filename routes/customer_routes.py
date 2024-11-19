from flask import Blueprint, request, jsonify
from services.customer_service import create_customer, remove_customer

bp = Blueprint('customer_routes', __name__)

@bp.route('/create_customer', methods=['POST'])
def create_customer_route():
    return create_customer(request.json)

@bp.route('/remove_customer', methods=['POST'])
def remove_customer_route():
    return remove_customer(request.json)
