from typing import Final
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
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
        if user.password != password:
            return Response(
                {"detail": f"Password is not correct. {password}, {user.password}"},
                status=HTTP_400_BAD_REQUEST,
            )
        token: Final[RefreshToken] = RefreshToken.for_user(user)
        refresh: Final[RefreshToken] = str(token)
        access: Final = str(token.access_token)
        response = Response({"user": user.id})
        response.set_cookie(key="refresh", value=refresh, httponly=True)
        response.set_cookie(key="access", value=access, httponly=True)
        return response


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        로그아웃
        POST /api/v1/users/logout
        """

        # get token from request cookie
        refresh: Final = request.data.get("refresh")
        if not refresh:
            raise ParseError("Refresh token is required.")
        # delete token from database
        try:
            token: Final = RefreshToken(refresh)
            token.blacklist()
        except Exception:
            raise ParseError("Refresh token is invalid.")
        # delete token from cookie
        response = Response({"status": True})
        response.delete_cookie("refresh")
        response.delete_cookie("access")
        return response
