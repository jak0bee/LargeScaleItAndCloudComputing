from flask import Flask
from routes import customer_routes, dish_routes

app = Flask(__name__)

# Register blueprints
app.register_blueprint(customer_routes.bp)
# app.register_blueprint(dish_routes.bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
