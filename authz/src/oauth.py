from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc7636 import CodeChallenge
from authlib.integrations.flask_oauth2 import (
    AuthorizationServer,
    ResourceProtector,
)
from mongomixin import Oauth2ClientMixin, OAuth2AuthorizationCodeMixin, OAuth2TokenMixin
from helper import (
    create_bearer_token_validator,
    create_query_client_func,
    create_revocation_endpoint,
    create_save_token_func
)

class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic',
        'client_secret_post',
        'none',
    ]


    def save_authorization_code(self, code, request):
        code_challenge = request.data.get('code_challenge')
        code_challenge_method = request.data.get('code_challenge_method')
        data = {
            "code":code,
            "client_id":request.client.client_id,
            "redirect_uri":request.redirect_uri,
            "scope":request.scope,
            "user_id":request.user.id,
            "code_challenge":code_challenge,
            "code_challenge_method":code_challenge_method,
        }
        auth_code = OAuth2AuthorizationCodeMixin(data)
        
        return auth_code




authorization = AuthorizationServer(
    query_client=create_query_client_func,
    save_token=create_save_token_func,
)
require_oauth = ResourceProtector()


def config_oauth(app):
    authorization.init_app(app)

    authorization.register_grant(AuthorizationCodeGrant, [CodeChallenge(required=True)])

    # support revocation
    revocation_cls = create_revocation_endpoint()
    authorization.register_endpoint(revocation_cls)

    # protect resource
    bearer_cls = create_bearer_token_validator()
    require_oauth.register_token_validator(bearer_cls())