from keycloak import KeycloakOpenID
from django.conf import settings

class KeycloakHelper:
    def __init__(self):
        self.keycloak_openid = KeycloakOpenID(
            server_url=settings.KEYCLOAK_CONFIG["SERVER_URL"],
            client_id=settings.KEYCLOAK_CONFIG["CLIENT_ID"],
            realm_name=settings.KEYCLOAK_CONFIG["REALM_NAME"],
            client_secret_key=settings.KEYCLOAK_CONFIG["CLIENT_SECRET"]
        )

    def get_token(self, username, password):
        try:
            return self.keycloak_openid.token(username, password)
        except Exception as e:
            return {"error": str(e)}

    def introspect_token(self, token):
        return self.keycloak_openid.introspect(token)

    def refresh_token(self, refresh_token):
        return self.keycloak_openid.refresh_token(refresh_token)
