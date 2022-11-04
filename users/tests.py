from typing import Final
from django.db import IntegrityError
from rest_framework.test import APITestCase
from rest_framework.response import Response
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
        user: Final = User.objects.create(
            username=self.VALIDED_USERNAME,
            email=self.VALIDED_USERNAME,
            password=self.VALIDED_PASSWORD,
        )
        self.assertEqual(user.email, self.VALIDED_USERNAME)


class TestUserView(APITestCase):
    def setUp(self) -> None:
        self.VALIDED_EMAIL = "valided@email.com"
        self.VALIDED_PASSWORD = "password"
        self.VALIDED_USER = User.objects.create(
            username=self.VALIDED_EMAIL + "2",
            email=self.VALIDED_EMAIL + "2",
            password=self.VALIDED_PASSWORD,
        )

    def test_signup(self):
        response: Final[Response] = self.client.post(
            "/api/v1/users/signup/",
            {
                "email": self.VALIDED_EMAIL,
                "password": self.VALIDED_PASSWORD,
            },
        )
        try:
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data["email"], self.VALIDED_EMAIL)
        except AssertionError as wrong:
            raise wrong(response.data)

    def test_login(self):
        login_data: Final = {
            "email": self.VALIDED_USER.email,
            "password": self.VALIDED_USER.password,
        }
        response: Final[Response] = self.client.post(
            "/api/v1/users/login/",
            login_data,
        )
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data["status"], True)
        except AssertionError as wrong:
            raise wrong(
                login_data,
                User.objects.get(username=self.VALIDED_USER.email),
                response.data,
            )

    def test_logout(self):
        self.client.force_login(self.VALIDED_USER)
        response: Final[Response] = self.client.get(
            "/api/v1/users/logout/",
        )
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data["status"], True)
        except AssertionError as wrong:
            raise wrong(response.data)
