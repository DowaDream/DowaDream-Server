from rest_framework.views import APIView
from django.http import JsonResponse
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .service import *
from .response import *
from .serializers import *


def responseFactory(res: ResponseDto):
    if res.data is None:
        return JsonResponse(status=res.status, data={ "msg": res.msg })
    else:
        return JsonResponse(
            status=res.status,
            data={ "msg": res.msg, "data": res.data }
        )

parameter_token = openapi.Parameter(
    "Authorization",
    openapi.IN_HEADER,
    description = "access_token",
    type = openapi.TYPE_STRING
)


class PrgmInteractUpdateView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SwaggerInteractSerializer
    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        responses= {
            200: message['PrgmInteractSuccess'],
            400: message['PrgmInteractFail'],
            401: '권한 없음'
        })
    def put(self, request):
        '''
            ## 봉사 스크랩하기/응원하기/내가 한 봉사 저장하기
            ![image](https://dowadream.s3.ap-northeast-2.amazonaws.com/20230813134434489_APISpecCapture2.png)
            - `progrmRegistNo` 필드는 필수입니다
            - `cheered`, `participated`, `clipped` 필드는 필수가 아닙니다.
            예를 들어 봉사번호 123445를 스크랩하려면 위의 사진처럼 request를 보내시면 됩니다
            - 스크랩 취소는 `"clipped": "False"`로 보내시면 됩니다.
        '''
        request.data['user'] = request.user.id
        res = update_progrm_interact(request.data, request.user)
        return responseFactory(res)


class CheeredGetView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        responses= {
            200: message['CheeredGetSuccess'],
            401: '권한 없음'
        })
    def get(self, request):
        '''
            ## 응원한 봉사 리스트 조회
        '''
        user = request.user
        interations_list = get_interactions_list(user, 'cheered')
        res = ResponseDto(status=200, data=interations_list, msg=message["CheeredGetSuccess"])
        return responseFactory(res)


class ParticipatedGetView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        responses= {
            200: message['ParticipatedGetSuccess'],
            401: '권한 없음'
        })
    def get(self, request):
        '''
            ## 참여한 봉사 리스트 조회
        '''
        user = request.user
        interations_list = get_interactions_list(user, 'participated')
        res = ResponseDto(status=200, data=interations_list, msg=message["ParticipatedGetSuccess"])
        return responseFactory(res)


class ClippedGetView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        responses= {
            200: message['ClippedGetSuccess'],
            401: '권한 없음'
        })
    def get(self, request):
        '''
            ## 스크랩한 봉사 리스트 조회
        '''
        user = request.user
        interations_list = get_interactions_list(user, 'clipped')
        res = ResponseDto(status=200, data=interations_list, msg=message["ClippedGetSuccess"])
        return responseFactory(res)