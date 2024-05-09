from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status


class AuthenticationTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testusername2",
            email="test2email@gmail.com",
            password="secretpassword",
        )

    def test_jwt_authentication(self):
        # Get JWT token
        response = self.client.post(
            "/api/token/",
            {"username": "testusername2", "password": "secretpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        """Making a request to a protected endpoint"""
        response = self.client.get("/api/purchase_orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
