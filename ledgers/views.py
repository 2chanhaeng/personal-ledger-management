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
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Ledger
from .serializers import (
    LedgersSerializer,
    LedgerDetailSerializer,
    LedgerCreateSerializer
)
from users.models import User


class LedgersView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request: Request) -> Response:
        """
        가계부 조회
        GET /api/v1/ledgers/
        """

        user: Final = request.user
        ledgers: Final = user.ledgers.all()
        serializer: Final = LedgersSerializer(ledgers, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        가계부 생성
        POST /api/v1/ledgers/
        """
        user: Final = request.user
        serializer: Final = LedgerCreateSerializer(
            data=request.data | {"user": user.id}
        )
        if not serializer.is_valid():
            raise ParseError(serializer.errors, code=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
