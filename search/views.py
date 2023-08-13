import json
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse, JsonResponse
from rest_framework import serializers
from .serializers import *
from .response import *

from search.service import *

class SearchKeywordView(APIView):
    @swagger_auto_schema(query_serializer=SearchKeywordSerializer, responses={"200":KeywordResponseSerializer, "404":KeywordResponseSerializer})
    def get(self, request):
        '''
            ## 키워드로 조회
            - `keyword`: 검색할 키워드
            - `actPlace`: 장소 (필수 필드 아님) Ex. 상도
        '''
        keyword = request.query_params.get('keyword')
        actPlace = request.query_params.get('actPlace')
        search_result = callByKeyword(keyword, actPlace)
        result = responseFactory(search_result)
        if search_result is None:
            return Response(result,status=status.HTTP_404_NOT_FOUND)
        return Response(result,status=status.HTTP_200_OK)


class SearchAreaView(APIView):
    @swagger_auto_schema(query_serializer=SearchAreaSerializer, responses={"200":AreaResponseSerializer, "404":AreaResponseSerializer})
    def get(self, request):
        '''
            ## 지역으로 조회
            - `keyword`: 지역코드(구군) Ex. 3120000
        '''
        keyword = request.query_params.get('keyword')
        search_result = callByArea(keyword)
        result = responseFactory(search_result)
        if search_result is None:
            return Response(result,status=status.HTTP_404_NOT_FOUND)
        return Response(result,status=status.HTTP_200_OK)


class SearchRegistNoView(APIView):
    @swagger_auto_schema(query_serializer=SearchRegistNoSerializer, responses={"200":RegistNoResponseSerializer, "404":RegistNoResponseSerializer})
    def get(self, request):
        '''
            ## 봉사ID(`progrmRegistNo`)으로 세부 봉사내용 조회
        '''
        keyword = request.query_params.get('keyword')
        search_result = callByRegistNo(keyword)
        result = responseFactory(search_result)
        if search_result is None:
            return Response(result,status=status.HTTP_404_NOT_FOUND)
        return Response(result,status=status.HTTP_200_OK)