from typing import Final, Dict
from rest_framework.response import Response
from rest_framework.test import APITestCase
from .models import Ledger
from .serializers import LedgerDetailSerializer, LedgersSerializer
from users.models import User


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

    def test_create_ledger(self):
        response: Final[Response] = self.client.post(
            "/api/v1/ledgers/",
            self.VALIDED_LEDGER_DATA,
            HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION,
            format="json",
        )
        try:
            self.assertEqual(response.status_code, 201)
        except AssertionError:
            raise AssertionError(
                f"Expected status code 201, but got {response.status_code}."
            )
        try:
            self.assertEqual(
                response.data["amount"],
                self.VALIDED_LEDGER_DATA["amount"]
            )
        except AssertionError:
            raise AssertionError(response.data)

    def test_get_ledgers(self):
        ledger: Final = Ledger.objects.create(
            user=self.VALIDED_USER,
            **self.VALIDED_LEDGER_DATA
        )
        response: Final[Response] = self.client.get(
            "/api/v1/ledgers/",
            HTTP_AUTHORIZATION=self.HTTP_AUTHORIZATION,
        )
        serialzed = LedgersSerializer(ledger)
        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError:
            raise AssertionError(
                f"The status code is {response.status_code}."
            )
        for name, data in serialzed.data.items():
            try:
                self.assertEqual(response.data[0].get(name), data)
            except AssertionError:
                raise AssertionError(
                    f"{name}: {data} != {response.data[0].get(name)}\n"
                    + f"{response.data}"
                )
