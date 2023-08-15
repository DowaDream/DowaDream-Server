from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class DefaultSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = []

class UserTagSerializer(ModelSerializer):
    class Meta:
        model = User_Tag
        fields = ['tags']

    tags = serializers.ListField(
        child=serializers.CharField(max_length=10),
        min_length=1,
        max_length=10
    )

class UserRegionSerializer(ModelSerializer):
    class Meta:
        model = User_Region
        fields = ["regions"]
    
    regions = serializers.ListField(
        child=serializers.CharField(max_length=20),
        min_length=1,
        max_length=10
    )