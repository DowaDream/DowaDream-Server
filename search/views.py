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
        keyword = request.query_params.get('keyword')
        search_result = callByArea(keyword)
        result = responseFactory(search_result)
        if search_result is None:
            return Response(result,status=status.HTTP_404_NOT_FOUND)
        return Response(result,status=status.HTTP_200_OK)


class SearchRegistNoView(APIView):
    @swagger_auto_schema(query_serializer=SearchRegistNoSerializer, responses={"200":RegistNoResponseSerializer, "404":RegistNoResponseSerializer})
    def get(self, request):
        keyword = request.query_params.get('keyword')
        search_result = callByRegistNo(keyword)
        result = responseFactory(search_result)
        if search_result is None:
            return Response(result,status=status.HTTP_404_NOT_FOUND)
        return Response(result,status=status.HTTP_200_OK)