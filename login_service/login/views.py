from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .keycloack_helper import KeycloakHelper

class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        keycloak_helper = KeycloakHelper()
        try:
            token_response = keycloak_helper.get_token(username, password)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if "error" in token_response:
            return Response(
                {"error": token_response["error"]},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(token_response, status=status.HTTP_200_OK)
