from flask import Flask, render_template, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
import logging
from dotenv import load_dotenv
import os
import copy
import jwt

class DataStore():
    user_info = None

data = DataStore()

load_dotenv()
app = Flask(__name__)
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
app.secret_key = os.getenv('secret_key')

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
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()
        data.user_info = copy.deepcopy(google_data)
    return render_template('index.j2',
                            google_data=google_data,
                            fetch_url=google.base_url + user_info_endpoint
                        )

@app.route('/login')
def login():
    return redirect(url_for('google.login'))

@app.route('/authorize')
def authz():
    
    print(data.user_info)
    return 'Test'

if __name__ == "__main__":
    app.run()