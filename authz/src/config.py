db_api_url = "http://authz-dbapi"
base_permissions = ["test"]
domain = "mperry.io"
allowed_permission = "web"
oauth_redirect_url = "http://auth.mperry.io/authorize"

DUMMY_JWT_CONFIG = {
    'key': 'secret-key',
    'alg': 'HS256',
    'iss': 'https://mperry.io',
    'exp': 3600,
}