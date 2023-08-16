from rest_framework.views import APIView
from django.http import JsonResponse
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from .service import *
from .response import *
from .serializers import *
from .dto import ProgramDto


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


### 봉사 추천 관련
from django.db.models import Count
class PrgmRecommendCheeringView(GenericAPIView):
    permission_classes = []

    def get(self, request):
        interactions = Program_Interaction.objects.filter(cheered=True).annotate(cheer_count=Count('cheered')).order_by('-cheer_count')
        progrmList = list(interactions.values_list('progrmRegistNo', flat=True))
        
        data = []
        for program in progrmList[:4]:
            p_data = callByRegistNo(program)
            # print(p_data, p_data['tagName'])
            program_dto_data = ProgramDto(tagName=p_data['tagName'], title=p_data['title'], registerInstitute=p_data['registerInstitute'], \
                                          recruitStart=p_data['recruitStart'], recruitEnd=p_data['recruitEnd'], actStart=p_data['actStart'], actEnd=p_data['actEnd'])
            data.append(program_dto_data.to_json())
        
        res = ResponseDto(status=200, data=data, msg=message['PrgrmRecommendCheer'])
        return responseFactory(res)



### 봉사 Interaction(응원, 스크랩, 참여)
class PrgmInteractUpdateView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SwaggerInteractSerializer
    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        message = "테스트",
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
    
class SearchKeywordView(APIView):
    # no permission needed
    permission_classes = []

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
        result = searchResponseFactory(search_result)
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