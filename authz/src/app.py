import secrets
from flask import Flask, render_template, redirect, session, url_for, Response, request, jsonify
from dotenv import load_dotenv
import os
from flask_dance.contrib.google import make_google_blueprint, google
from authlib.oauth2 import OAuth2Error
from mongomixin import Oauth2ClientMixin 
from oauth import authorization, require_oauth, generate_user_info, config_oauth
from model import User
from helper import user_exists, create_json_user, get_user_by_id
from mock_info import fake_user
import json
from authlib.integrations.flask_oauth2 import current_token

load_dotenv()
app = Flask(__name__)
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
app.secret_key = secrets.token_urlsafe(32)

app.config.from_pyfile("settings.py")
config_oauth(app)
#need to do something else
os.environ['OAUTHLIB_INSECURE_TRANSPORT']='1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE']='1'

blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email", "openid"],
    redirect_url="/authorize"
    )

app.register_blueprint(blueprint, url_prefix="/login")

@app.route('/login')
def login():
    return redirect(url_for('google.login'))

@app.route('/logout') 
def logout():
    session.pop('User', None)

@app.route('/userinfo')
@require_oauth('profile')
def permissions():
    return jsonify(generate_user_info(current_token.user_id, current_token.scope))

@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    user_info_endpoint = '/oauth2/v2/userinfo'
    if not google.authorized:
        session['query_str'] = request.query_string
        return redirect(url_for("google.login", next=request.url))
    if request.query_string == b'':
        request.query_string = session['query_str']
    session['User'] = google.get(user_info_endpoint).json()  
    authz_user = user_exists(session['User'])
    if authz_user is not None:
        user = User(json.loads(authz_user))
    else:
        user = User(json.loads(create_json_user(session['User'])))
    if request.method == 'GET':
        try:
            _ = authorization.validate_consent_request(end_user=user)
        except OAuth2Error as error:
            return jsonify(dict(error.get_body()))
    return authorization.create_authorization_response(grant_user=user)


@app.route('/token/', methods=['POST'])
def token():
    return authorization.create_token_response()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8060)