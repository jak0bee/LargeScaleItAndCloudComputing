from flask import Flask
from routes import customer_routes, dish_routes
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


# Register blueprints
app.register_blueprint(customer_routes.bp, url_prefix='/api/customers')
app.register_blueprint(dish_routes.dish_blueprint, url_prefix='/api/dish')






if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
