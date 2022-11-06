from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")

    def validate(self, attrs):
        email = attrs.get("email")
        if not email:
            raise serializers.ValidationError("Email is required.")
        password = attrs.get("password")
        if not password:
            raise serializers.ValidationError("Password is required.")
        attrs["username"] = email
        return attrs
