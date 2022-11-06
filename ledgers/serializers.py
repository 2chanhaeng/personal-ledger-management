from rest_framework import serializers
from .models import Ledger


class LedgersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ledger
        fields = ("amount", "memo", "created_at")
