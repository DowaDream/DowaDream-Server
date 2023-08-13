from rest_framework.serializers import ModelSerializer
from .models import User

class DefaultSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = []