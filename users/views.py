from typing import Final
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework.status import HTTP_400_BAD_REQUEST
from .models import User
from .serializers import UserSerializer


class SignUpView(APIView):
    def post(self, request: Request) -> Response:
        """
        회원가입
        POST /api/v1/users
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
        return Response(serializer.data)
