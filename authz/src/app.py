import secrets
from flask import Flask, redirect, session, url_for, request, jsonify, render_template
from dotenv import load_dotenv
import os
from flask_dance.contrib.google import make_google_blueprint, google
from authlib.oauth2 import OAuth2Error
from oauth import authorization, require_oauth, generate_user_info, config_oauth
from model import User
from helper import user_exists, create_json_user
import json
from authlib.integrations.flask_oauth2 import current_token
import time
from config import custom_redirect_url

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
os.environ['AUTHLIB_INSECURE_TRANSPORT']='1'

blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email", "openid"],
    redirect_url=custom_redirect_url
    )

app.register_blueprint(blueprint, url_prefix="/login")

@app.route('/login')
def login():
    return redirect(url_for('google.login'))

@app.route('/logout') 
def logout():
    if blueprint.token is not None:
        token = blueprint.token["access_token"]
        resp = google.post(
            "https://accounts.google.com/o/oauth2/revoke",
            params={"token": token},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        del blueprint.token
    session.pop('User', None)
    
    return render_template('loggedout.html')

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
    elif request.query_string == b'':
        request.query_string = session['query_str']
    token_expire_time = blueprint.token['expires_at']
    if int(time.time()) >= token_expire_time:
        return redirect(url_for("logout"))
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

@app.route('/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_endpoint_response('revocation')

@app.route('/token/', methods=['POST'])
def token():
    return authorization.create_token_response()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8060)