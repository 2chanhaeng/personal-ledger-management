from typing import Final
from django.db import IntegrityError
from rest_framework.test import APITestCase
from .models import User


class TestUserModel(APITestCase):
    def setUp(self) -> None:
        self.VALIDED_USERNAME = "valided_username"
        self.VALIDED_EMAIL = "valided_email@valided_email.com"
        self.VALIDED_PASSWORD = "password"

    def test_create_user(self):
        try:
            self.unvailded_email_user = User.objects.create(
                username="unvailded_username",
                email="unvailded_email",
                password="password",
            )
        except IntegrityError:
            pass
        except Exception as e:
            raise e
        else:
            AssertionError("unvailded_email_user is created.")
        user = User.objects.create(
            username=self.VALIDED_USERNAME,
            email=self.VALIDED_USERNAME,
            password=self.VALIDED_PASSWORD,
        )
        self.assertEqual(user.email, self.VALIDED_USERNAME)


class TestUserView(APITestCase):
    def setUp(self) -> None:
        self.VALIDED_USERNAME = "valided_username"
        self.VALIDED_EMAIL = "valided_email@valided_email.com"
        self.VALIDED_PASSWORD = "password"

    def test_signup(self):
        response = self.client.post(
            "/api/v1/users/signup/",
            {
                "username": self.VALIDED_USERNAME,
                "email": self.VALIDED_EMAIL,
                "password": self.VALIDED_PASSWORD,
            },
        )
        try:
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data["email"], self.VALIDED_EMAIL)
        except AssertionError as e:
            print(response.data)
            raise e

    def test_login(self):
        response = self.client.post(
            "/api/v1/users/login/",
            {
                "email": self.VALIDED_EMAIL,
                "password": self.VALIDED_PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], True)

    def test_logout(self):
        response = self.client.post(
            "/api/v1/users/logout/",
            {
                "email": self.VALIDED_EMAIL,
                "password": self.VALIDED_PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], True)
