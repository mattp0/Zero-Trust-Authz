import secrets
from flask import Flask, render_template, redirect, session, url_for, Response, request, jsonify
from dotenv import load_dotenv
import os
from flask_dance.contrib.google import make_google_blueprint, google
from authlib.oauth2 import OAuth2Error
from mongomixin import Oauth2ClientMixin 
from config import email_scope
from authlib.integrations.flask_oauth2 import current_token
from oauth import authorization, require_oauth, generate_user_info, config_oauth
from model import User
from mock_info import fake_user

load_dotenv()
app = Flask(__name__)
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
app.secret_key = secrets.token_urlsafe(32)

app.config.from_pyfile("settings.py")
config_oauth(app)
#need to do something else
called_request = None
os.environ['OAUTHLIB_INSECURE_TRANSPORT']='1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE']='1'

blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email", "openid"]
    )

app.register_blueprint(blueprint, url_prefix="/login")

@app.route('/')
def home():
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        session['User'] = google.get(user_info_endpoint).json()
        return render_template('index.j2',
                            google_data=session['User'],
                            fetch_url=google.base_url + user_info_endpoint
                        )
    return redirect(url_for("login"))

@app.route('/login')
def login():
    return redirect(url_for('google.login'))


@app.route('/logout') 
def logout():
    session.pop('User', None)

@app.route('/userinfo')
# @require_oauth('profile')
def permissions():
    print("inside user info!")
    user = User(fake_user)

    return jsonify(generate_user_info(user, "openid profile email"))

@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    print(authorization._authorization_grants)
    print('got a authroize request')
    print(request.query_string)
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        session['User'] = google.get(user_info_endpoint).json()
    if "User" not in session:
        return redirect(url_for("google.login", next=request.url))
    user = User(session['User'])
    print("user created", user)
    if request.method == 'GET':
        print("got a get request")
        try:
            print("trying to get a grant")
            grant = authorization.validate_consent_request(end_user=user)
            print(grant)
            print(type(grant))
        except OAuth2Error as error:
            return jsonify(dict(error.get_body()))
        return render_template('authorize.html', user=user, grant=grant)
    print("got a post")
    if request.form['confirm']:
        grant_user = user
    else:
        grant_user = None
    return authorization.create_authorization_response(grant_user=grant_user)


@app.route('/token/', methods=['POST'])
def token():
    print("we got a post to token")
    print(request.form)
    return authorization.create_token_response()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8060)