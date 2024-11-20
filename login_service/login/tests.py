from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/login/login/"  

    @patch("login.keycloack_helper.KeycloakHelper.get_token")
    def test_login_successful(self, mock_get_token):
        # Mock KeycloakHelper response
        mock_get_token.return_value = {
            "access_token": "mock_access_token",
            "refresh_token": "mock_refresh_token",
            "expires_in": 3600,
        }

        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.url, data)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    @patch("login.keycloack_helper.KeycloakHelper.get_token")
    def test_login_failure_invalid_credentials(self, mock_get_token):
        # Mock KeycloakHelper response for invalid credentials
        mock_get_token.return_value = {"error": "invalid_grant"}

        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.url, data)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "invalid_grant")

    def test_login_missing_fields(self):
        # Test missing username
        data = {"password": "testpassword"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Username and password are required.")


        data = {"username": "testuser"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Username and password are required.")

    @patch("login.keycloack_helper.KeycloakHelper.get_token")
    def test_keycloak_service_error(self, mock_get_token):
        # Mock KeycloakHelper to simulate an internal error
        mock_get_token.side_effect = Exception("Keycloak service is unavailable")

        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.url, data)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["error"], "Keycloak service is unavailable")
