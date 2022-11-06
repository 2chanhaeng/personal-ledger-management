from typing import Final, Dict
from rest_framework.response import Response
from rest_framework.test import APITestCase
from .models import Ledger
from .serializers import LedgerDetailSerializer, LedgersSerializer
from users.models import User

# Create your tests here.

class LedgersViewTest(APITestCase):
    def get_login_cookies(self) -> Dict[str, str]:
        LOGIN_DATA: Final = {
            "email": self.VALIDED_USER.email,
            "password": self.VALIDED_USER.password,
        }
        response: Final[Response] = self.client.post(
            "/api/v1/users/login/",
            LOGIN_DATA,
        )
        cookies: Final = response.cookies
        return {
            "refresh": cookies["refresh"].value,
            "access": cookies["access"].value,
        }

    def setUp(self) -> None:
        self.VALIDED_EMAIL = "valided@email.com"
        self.VALIDED_USER = User.objects.create(
            username=self.VALIDED_EMAIL,
            email=self.VALIDED_EMAIL,
            password="password",
        )
        self.VALIDED_LEDGER_DATA = {
            "amount": 1000,
            "memo": "memo",
            "info": {
                "info1": "info_data1",
            },
        }
        self.COOKIES = self.get_login_cookies()
        self.ACCESS = self.COOKIES.get("access")
        self.REFRESH = self.COOKIES.get("refresh")
        self.HTTP_AUTHORIZATION = f"Bearer {self.ACCESS}"
