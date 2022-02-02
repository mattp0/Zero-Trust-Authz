import secrets
from flask import Flask, render_template, redirect, session, url_for, Response
from dotenv import load_dotenv
import os
from flask_dance.contrib.google import make_google_blueprint, google

from helper import create_json_user, user_exists
from config import email_scope


load_dotenv()
app = Flask(__name__)
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
app.secret_key = secrets.token_urlsafe(32)

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

@app.route('/permissions')
def permissions():
    pass

@app.route('/authorize')
def authorize():
    pass

@app.route('/token')
def token():
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8060)