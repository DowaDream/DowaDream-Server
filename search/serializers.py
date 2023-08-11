from .models import *
from rest_framework import serializers

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


# class KeywordQuerySerializer(serializers.Serializer):
#     # keyword = serializers.ListField(child=serializers.CharField())
#     # actPlace = serializers.ListField(child=serializers.CharField(), required=False)
#     class Meta:
#         model = KeywordQuery
#         fields = '__all__'
#     keyword = serializers.ListField(child=serializers.CharField())
#     actPlace = serializers.ListField(child=serializers.CharField(), required=False)

# class AreaQuerySerializer(serializers.Serializer):
#     keyword = serializers.ListField(child=serializers.CharField())

# class RegistNoQuerySerializer(serializers.Serializer):
#     registNo = serializers.ListField(child=serializers.CharField())

# class SearchResponseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SearchResponse    # 어떤 모델을 serialize할 것인지
#         fields = ['status', 'message', 'data']
    # data = serializers.ListField(child=serializers.DictField())
