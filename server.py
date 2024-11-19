# server.py
from flask import Flask
from routes.dish_routes import dish_blueprint  # Ensure this is correct

app = Flask(__name__)
app.register_blueprint(dish_blueprint, url_prefix='/dish')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
