from flask import Blueprint, request, jsonify, redirect, url_for, session
from requests_oauthlib import OAuth2Session

bp = Blueprint('auth', __name__)

# OAuth2 configuration
CLIENT_ID = '2ca545cff72c86c46b35194bc2440d728bbf22c7141675672f7006d422b1fc7f'
CLIENT_SECRET = 'gloas-6e880c0b10efa99a5b245e6addc6addc9e1001c414f370705d588b90acb03870'
AUTHORIZATION_BASE_URL = 'https://gitlab.com/oauth/authorize'
TOKEN_URL = 'https://gitlab.com/oauth/token'
API_BASE_URL = 'https://gitlab.com/api/v4'

# This will be dynamically set based on the incoming request
def get_redirect_uri():
    # Dynamically build the redirect URI based on the incoming request
    return f"{request.scheme}://{request.host}/login/oauth2/code/gitlab"

# Create an OAuth2 session
def create_oauth_session():
    redirect_uri = get_redirect_uri()  # Dynamically set the redirect URI
    oauth = OAuth2Session(
        CLIENT_ID,
        redirect_uri=redirect_uri,
        scope=["openid", "profile", "email"]
    )
    return oauth

@bp.route('/login', methods=['GET'])
def login():
    """
    GitLab OAuth2 Login
    """
    oauth = create_oauth_session()
    authorization_url, state = oauth.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth_state'] = state
    return redirect(authorization_url)

@bp.route('/login/oauth2/code/gitlab', methods=['GET'])
def login_callback():
    """
    GitLab OAuth2 Login Callback
    """
    code = request.args.get('code')
    state = request.args.get('state')

    try:
        oauth = create_oauth_session()
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
    return redirect("/apidocs")

@bp.route('/profile', methods=['GET'])
def profile():
    """
    Retrieve User Profile
    """
    if 'user_info' in session:
        return jsonify(session['user_info'])
    else:
        return redirect(url_for('.login'))

@bp.route('/logout', methods=['GET'])
def logout():
    """
    Logout
    """
    session.clear()
    return redirect(url_for('.login'))
