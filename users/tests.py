from typing import Final
from django.db import IntegrityError
from rest_framework.test import APITestCase
from .models import User


class TestUserModel(APITestCase):
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
        VALIDED_EMAIL: Final = "valided_email@valided_email.com"
        user = User.objects.create(
            username="valided_username",
            email=VALIDED_EMAIL,
            password="password",
        )
        print("test_create_user", user.username)
        self.assertEqual(user.email, VALIDED_EMAIL)


class TestUserView(APITestCase):
    def setUp(self) -> None:
        self.VALIDED_USERNAME = "valided_username"
        self.VALIDED_EMAIL = "valided_email@valided_email.com"
        self.VALIDED_PASSWORD = "password"
