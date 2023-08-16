from rest_framework import serializers
from .models import Program_Interaction


class PrgmInteractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program_Interaction
        fields = "__all__"  # 모든 필드를 가져오기

class SwaggerInteractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program_Interaction
        exclude = ['user']

class SearchKeywordSerializer(serializers.Serializer):
    keyword = serializers.CharField()
    actPlace = serializers.CharField(required=False)

class SearchAreaSerializer(serializers.Serializer):
    keyword = serializers.CharField()
    
class SearchRegistNoSerializer(serializers.Serializer):
    keyword = serializers.CharField(required=True)
    
class KeywordDictSerializer(serializers.Serializer):
    title = serializers.CharField()
    place = serializers.CharField()
    progrmRegistNo = serializers.CharField()

class KeywordResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()
    data = KeywordDictSerializer(many=True)

class AreaDictSerializer(serializers.Serializer):
    title = serializers.CharField()
    progrmRegistNo = serializers.CharField()

class AreaResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()
    data = AreaDictSerializer(many=True)

class RegistNoDictSerializer(serializers.Serializer):
    title = serializers.CharField()
    recruitStatusNm = serializers.CharField()
    actStart = serializers.CharField()
    actEnd = serializers.CharField()
    place = serializers.CharField()
    adultAble = serializers.CharField()
    teenAble = serializers.CharField()
    recruitStart = serializers.CharField()
    recruitEnd = serializers.CharField()
    recruitInstitute = serializers.CharField()
    registerInstitute = serializers.CharField()
    maxPerson = serializers.CharField()
    content = serializers.CharField()
    progrmRegistNo = serializers.CharField()

class RegistNoResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()
    data = RegistNoDictSerializer(many=True)