from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse


from search.service import *

def responseFactory(result):
    if result is None:
        return '404', 'Not Found'
    else:
        return '200', 'OK'

@api_view(['POST'])
def search_keyword(request): # return as json

    keyword = request.data.get('keyword')
    actPlace = request.data.get('actPlace')
    search_result = callByKeyword(keyword, actPlace)
    code, msg = responseFactory(search_result)
    result = {
        'status': code,
        'message': msg,
        'data': search_result
    }
    return Response(result)


@api_view(['POST'])
def search_area(request): # return as json

    keyword = request.data.get('keyword')

    search_result = callByArea(keyword)
    code, msg = responseFactory(search_result)
    result = {
        'status': code,
        'message': msg,
        'data': search_result
    }
    return Response(result)


@api_view(['POST'])
def search_regist_no(request): # return as json

    progrmRegistNo = request.data.get('keyword')
    search_result = callByRegistNo(progrmRegistNo)
    code, msg = responseFactory(search_result)
    result = {
        'status': code,
        'message': msg,
        'data': search_result
    }
    return Response(result)