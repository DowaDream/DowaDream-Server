from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'email', 'age']