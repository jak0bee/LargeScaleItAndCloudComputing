from functools import wraps

from flask import Blueprint, request, jsonify, redirect, url_for, session
from requests_oauthlib import OAuth2Session

bp = Blueprint('auth', __name__)

# OAuth2 configuration
CLIENT_ID = '076f9e789fac2f361c2e0145aa0cc7298cd6c5455492f3c90999480e40406d3f'
CLIENT_SECRET = 'gloas-2b635dc4bf910399e28ed5ede32d88305bc7ebf6450150ee8a3cac4078fecf91'
AUTHORIZATION_BASE_URL = 'https://gitlab.com/oauth/authorize'
TOKEN_URL = 'https://gitlab.com/oauth/token'
API_BASE_URL = 'https://gitlab.com/api/v4'
REDIRECT_URI = "http://localhost:8080/login/oauth2/code/gitlab"

# Create an OAuth2 session
oauth = OAuth2Session(
    CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    scope=["openid", "profile", "email"]
)

@bp.route('/login', methods=['GET'])
def login():
    """
    GitLab OAuth2 Login
    ---
    tags:
      - Authentication
    responses:
      302:
        description: Redirects to GitLab OAuth2 login
    """
    authorization_url, state = oauth.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth_state'] = state
    return redirect(authorization_url)

@bp.route('/login/oauth2/code/gitlab', methods=['GET'])
def login_callback():
    """
    GitLab OAuth2 Login Callback
    ---
    tags:
      - Authentication
    parameters:
      - name: code
        in: query
        type: string
        required: true
        description: The authorization code returned by GitLab
      - name: state
        in: query
        type: string
        required: false
        description: The state returned by GitLab
    responses:
      302:
        description: Redirects to the profile page or original destination
      400:
        description: Returns an error message if authentication fails
    """
    code = request.args.get('code')
    state = request.args.get('state')

    try:
        token = oauth.fetch_token(
            TOKEN_URL,
            authorization_response=request.url,
            client_secret=CLIENT_SECRET,
            verify=False
        )
        user_info_response = oauth.get("https://gitlab.com/oauth/userinfo", verify=False)
        session['user_info'] = user_info_response.json()
    except Exception as e:
        return f"Error: {e}", 400

    # Check if there is a 'next' URL stored in the session, and redirect there
    next_url = session.pop('next', None)
    if next_url:
        return redirect(next_url)

    # If there's no stored 'next' URL, redirect to the profile page
    return redirect(url_for('.profile'))


@bp.route('/profile', methods=['GET'])
def profile():
    """
    Retrieve User Profile
    ---
    tags:
      - Authentication
    responses:
      200:
        description: Returns the authenticated user's profile information
        schema:
          type: object
          properties:
            email:
              type: string
              example: "user@example.com"
            email_verified:
              type: boolean
              example: true
            name:
              type: string
              example: "John Doe"
            nickname:
              type: string
              example: "johnny"
            picture:
              type: string
              example: "https://gitlab.com/uploads/-/system/user/avatar/1/avatar.png"
      302:
        description: Redirects to the login page if the user is not authenticated
    """
    if 'user_info' in session:
        return jsonify(session['user_info'])
    else:
        return redirect(url_for('.login'))

@bp.route('/logout', methods=['GET'])
def logout():
    """
    Logout
    ---
    tags:
      - Authentication
    responses:
      302:
        description: Clears the session and redirects to the login page
    """
    session.clear()
    return redirect(url_for('.login'))
