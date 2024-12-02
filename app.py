from flask import Flask, request, session, redirect, url_for
from routes import customer_routes, dish_routes, auth
from flasgger import Swagger
import os


app = Flask(__name__)
swagger = Swagger(app)

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(customer_routes.bp, url_prefix='/api/customers')
app.register_blueprint(dish_routes.dish_blueprint, url_prefix='/api/dish')

# Ensures authorization
@app.before_request
def enforce_authorization_rules():
    # Define your protected endpoints
    protected_routes = [
        ("/api", ["GET"]),
        ("/api", ["POST"]),
    ]

    # Allow unauthenticated access to certain paths
    public_routes = ["/login", "/"]

    # Check if the request is public or needs authentication
    if request.path not in public_routes:
        # Check if the route is protected
        for route, methods in protected_routes:
            if request.path.startswith(route) and request.method in methods:
                # Enforce authentication
                if 'user_info' not in session:
                    # Save the original path in session
                    session['next'] = request.url
                    return redirect(url_for("auth.login"))  # Redirect if not authenticated

    # Permit all other requests
    return None


if __name__ == "__main__":
    # Disable the HTTPS requirement for OAuth2 (use only for development)
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Relax token scope enforcement
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', port=8080)
