from typing import Final
from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from .models import User
from .serializers import UserSerializer


class SignUpView(APIView):
    def post(self, request: Request) -> Response:
        """
        회원가입
        POST /api/v1/users/signup/
        """

        password: Final = request.data.get("password")
        serializer: UserSerializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            # if serializer is not valid, return 400 bad request
            # TODO: specify error message
            return Response({"detail": serializer.errors}, status=HTTP_400_BAD_REQUEST)
        user: User = serializer.save()
        user.set_password(password)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request: Request) -> Response:
        """
        로그인
        POST /api/v1/users/login
        """

        email: Final = request.data.get("email")
        if not email:
            raise ParseError("Email is required.")
        password: Final = request.data.get("password")
        if not password:
            raise ParseError("Password is required.")
        # request.data["username"] = email
        filtered_user: Final = User.objects.filter(email=email)
        if not filtered_user.exists():
            return Response(
                {"detail": f"User with email {email} does not exist."},
                status=HTTP_404_NOT_FOUND,
            )
        user: Final = filtered_user.first()
        if not user.check_password(password):
            return Response(
                {"detail": "Password is not correct."},
                status=HTTP_400_BAD_REQUEST,
            )
        login(request, user)
        # TODO: create JWT token and response
        return Response({"status": True})


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        로그아웃
        GET /api/v1/users/logout
        """
        logout(request)
        return Response({"status": True})
