from rest_framework import serializers
from .models import Program_Interaction


class PrgmInteractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program_Interaction
        fields = "__all__"  # 모든 필드를 가져오기