from flask import Blueprint, request, jsonify
from services.customer_service import create_customer, remove_customer

bp = Blueprint('customer_routes', __name__)

@bp.route('/create_customer', methods=['POST'])
def create_customer_route():
    """
Creating new customer and assigning him unique identifier
---
tags:
  - Customer Management
parameters:
  - name: customer_name
    in: path
    type: string
    required: true
    description: The name of the customer
responses:
  200:
    description: Success
    schema:
      type: object
      properties:
        message:
          type: string
          example: "Customer created successfully!"
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
def remove_customer_route():
    """
Creating new customer and assigning him unique identifier
---
tags:
  - Customer Management
parameters:
  - name: customer_name
    in: path
    type: string
    required: true
    description: The name of the customer
responses:
  200:
    description: Success
    schema:
      type: object
      properties:
        message:
          type: string
          example: "Customer created successfully!"
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
