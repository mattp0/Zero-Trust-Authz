meta = {
    "redirect_uris": ["http://localhost/auth"],
    "token_endpoint_auth_method": "client_secret_basic",
    "grant_types": ["authorization_code"],
    "response_types": ["code"],
    "client_name": "The Main Frame",
    "client_uri": "http://localhost",
    "scope": "openid profile email",
}

client_info = {
    "client_id":"123456789",
    "client_secret":"123456",
    "client_id_issued_at": 1644093866,
    "client_secret_expires_at": 1644193866,
}

token_info = {
    "client_id":"123456789",
    "token_type":"Bearer",
    "access_token":"secret",
    "refresh_token":"secret",
    "scope":"openid profile email",
    "issued_at": 1644093866,
    "access_token_revoked_at": 1644193866,
    "refresh_token_revoked_at": 1644193866,
    "expires_in": 860000,
}

auth_code_info = {
    "code":"123456789",
    "client_id":"123456",
    "redirect_uri":"http://localhost/auth",
    "response_type":"code",
    "scope":"openid profile email",
    "nonce":"secret",
    "auth_time": 1644193866
}

fake_user = {'id': '105757039183670861408', 'email': 'mperry37@alaska.edu', 'verified_email': True, 'name': 'Matt Perry', 'given_name': 'Matt', 'family_name': 'Perry', 'link': 'https://plus.google.com/105757039183670861408', 'picture': 'https://lh3.googleusercontent.com/a-/AOh14Gg2PwJ-XhmUM_nnQuuRuWuBZZo2cf0Bq1P56kk6iA=s96-c', 'locale': 'en', 'hd': 'alaska.edu'}