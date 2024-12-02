from flask import Blueprint, request, jsonify
from services.customer_service import create_customer, remove_customer
from utils.auth_utils import customer_role_required

bp = Blueprint('customer_routes', __name__)

@bp.route('/create_customer', methods=['POST'])
@customer_role_required
def create_customer_route():
    """
    Adding a customer
    ---
    tags:
      - Add customer
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            customer_name:
              type: string
              description: The name of the customer
              example: "Filip"
    responses:
      200:
        description: Success
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User added succesfully"
      400:
        description: Failure
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Missing required parameters"
    """

    return create_customer(request.json)

@bp.route('/remove_customer', methods=['POST'])
@customer_role_required
def remove_customer_route():
    """
    removing a customer
    ---
    tags:
      - remove customer
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            customer_id:
              type: string
              description: The name of the customer
              example: "0"
    responses:
      200:
        description: Success
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User added succesfully"
      400:
        description: Failure
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Missing required parameters"
    """

    return remove_customer(request.json)
