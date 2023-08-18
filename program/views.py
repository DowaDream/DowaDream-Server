from rest_framework.views import APIView
from django.http import JsonResponse
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
import threading

from .service import *
from .search_service import *
from .response import *
from .serializers import *
# from .search_service import *


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

def callAndAddRes(storage, keyword, actPlace, tagCode, areaCode):
    temp = callByKeyword(keyword, actPlace, tagCode, areaCode)
    if temp is not None:
        storage += temp


### 봉사 추천 관련
class PrgmRecommendCheeringView(GenericAPIView):
    permission_classes = []

    @swagger_auto_schema(
        responses= {
            200: message['PrgrmRecommendCheer']
        })
    def get(self, request):
        '''
            ## 봉사 추천: 응원하기 가장 많은 봉사 4개
        '''
        res = get_cheer_recommend()
        return responseFactory(res)



### 봉사 Interaction(응원, 스크랩, 참여)
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
            - `progrmRegistNo` 필드는 필수입니다
            - `cheered`, `participated`, `clipped` 필드는 필수가 아닙니다.
            예를 들어 봉사번호 123445를 스크랩하려면 
            { "progrmRegistNo": "123445", "clipped": "True" }
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
            ## 로그인한 유저가 응원한 봉사 리스트 조회
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
            ## 로그인한 유저가 참여한 봉사 리스트 조회
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
            ## 로그인한 유저가 스크랩한 봉사 리스트 조회
        '''
        user = request.user
        interations_list = get_interactions_list(user, 'clipped')
        res = ResponseDto(status=200, data=interations_list, msg=message["ClippedGetSuccess"])
        return responseFactory(res)
    
class SearchKeywordView(APIView):
    # no permission needed
    permission_classes = []

    @swagger_auto_schema(query_serializer=SearchKeywordSerializer, responses={"200":KeywordResponseSerializer, "404":KeywordResponseSerializer})
    def get(self, request):
        '''
            ## 봉사 조회: 키워드로 조회
            - `keyword`: 검색할 키워드
            - `actPlace`: 장소 (필수 필드 아님) Ex. 상도
            - `tagCode`: 분야코드 (필수 필드 아님) Ex. 0101
            - `areaCode`: 지역코드 (필수 필드 아님) Ex. 3510000
        '''
        keyword = request.query_params.get('keyword')
        actPlace = request.query_params.get('actPlace')
        tagCodes = request.query_params.getlist('tagCode')
        areaCodes = request.query_params.getlist('areaCode')

        search_result = []
        threads = []
        # print(f"tagCodes: {tagCodes}, areaCodes: {areaCodes}")
        print("tagcodes:", tagCodes, "areacodes:", areaCodes)
        # convert tagCodes, areaCodes to list
        if len(tagCodes) == 0:
            tagCodes = None
        if len(areaCodes) == 0:
            areaCodes = None

        # 둘 다 none 일 때
        if tagCodes is None and areaCodes is None:
            thread = threading.Thread(target=callAndAddRes, args=(search_result,keyword, actPlace, None, None))
            thread.start()
            threads.append(thread)

        # 둘 중 하나가 none 일 때
        elif tagCodes is None and areaCodes is not None:
            for areaCode in areaCodes:
                thread = threading.Thread(target=callAndAddRes, args=(search_result,keyword, actPlace, None, areaCode))
                thread.start()
                threads.append(thread)
        elif areaCodes is None and tagCodes is not None:
            for tagCode in tagCodes:
                thread = threading.Thread(target=callAndAddRes, args=(search_result,keyword, actPlace, tagCode, None))
                thread.start()
                threads.append(thread)

        # 둘 다 none 이 아닐 때
        else:
            for tagCode in tagCodes:
                for areaCode in areaCodes:
                    # 비동기로 요청
                    thread = threading.Thread(target=callAndAddRes, args=(search_result,keyword, actPlace, tagCode, areaCode))
                    thread.start()
                    threads.append(thread)                
        
        # 모든 서버가 끝날때까지 대기
        for thread in threads:
            thread.join()

        result = searchResponseFactory(search_result)

        if search_result is None:
            return Response(result,status=status.HTTP_404_NOT_FOUND)
        return Response(result,status=status.HTTP_200_OK)


class SearchAreaView(APIView):
    @swagger_auto_schema(query_serializer=SearchAreaSerializer, responses={"200":AreaResponseSerializer, "404":AreaResponseSerializer})
    def get(self, request):
        '''
            ## 봉사 조회: 지역으로 조회
            - `keyword`: 지역코드(구군) Ex. 3120000
        '''
        keyword = request.query_params.get('keyword')
        search_result = callByArea(keyword)
        result = searchResponseFactory(search_result)
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
        result = searchResponseFactory(search_result)
        if search_result is None:
            return Response(result,status=status.HTTP_404_NOT_FOUND)
        return Response(result,status=status.HTTP_200_OK)
    
class SearchDdayView(APIView):
    @swagger_auto_schema(responses={"200":DdayResponseSerializer, "404":DdayResponseSerializer})
    def get(self, request):
        '''
            ## 마감임박순으로 세부 봉사내용 조회
        '''
        search_result = callByDday()
        result = searchResponseFactory(search_result)
        if search_result is None:
            return Response(result,status=status.HTTP_404_NOT_FOUND)
        return Response(result,status=status.HTTP_200_OK)


### 유저 게이지 관련
class UserGaugeView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        responses= {
            200: message['ClippedGetSuccess'],
            401: '권한 없음'
        })
    def get(self, request):
        '''
            ## 게이지 조회
            - my_gauge: 로그인한 유저의 게이지
            - best_gauge: 가장 높은 유저의 게이지
            - total_gauge: 모든 유저의 게이지 총합
        '''
        res = get_user_gauge(request.user)
        return responseFactory(res)