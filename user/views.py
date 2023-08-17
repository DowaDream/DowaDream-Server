from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google import views as google_view
from requests import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from django.core.serializers import serialize


from .service import *
from .models import *
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


# 구글 로그인
# def google_login(request):
#     scope = "https://www.googleapis.com/auth/userinfo.email "
#     client_id = settings.GOOGLE_CLIENT_ID
#     return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


# Callback 함수
# def google_callback(request):
#     code = request.GET.get('code')
#     access_token = get_google_access_token(code)
#     print(access_token)
#     return access_token
    # email, profile_img = get_google_profile(access_token)

    # try:
    #     user = User.objects.get(email=email)

    #     # 이미 Google로 제대로 가입된 유저 => 로그인
    #     data = {'access_token': access_token, 'code': code}
    #     res = google_callback_signin(data, user, email)
    #     return responseFactory(res)

    # except User.DoesNotExist:   # 회원가입
    #     data = {'access_token': access_token, 'code': code}
    #     res = google_callback_signup(data, email, profile_img)
    #     return responseFactory(res)


import json
class AccessTokenView(GenericAPIView):
    def post(self, request):
        try:
            raw_data = request.body
            decoded_data = raw_data.decode('utf-8')
            json_data = json.loads(decoded_data)

            google_access_token = json_data.get('access_token')
            if google_access_token:
                email, profile_img = get_google_profile(google_access_token)
                try:
                    user = User.objects.get(email=email)

                    # 이미 Google로 제대로 가입된 유저 => 로그인
                    res = google_callback_signin(user, email)
                    return responseFactory(res)

                except User.DoesNotExist:   # 회원가입
                    res = google_callback_signup(email, profile_img)
                return responseFactory(res)
            else:
                return Response({"error": "Access token not found in request body."}, status=status.HTTP_400_BAD_REQUEST)

        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format in request body."}, status=status.HTTP_400_BAD_REQUEST)


# class GoogleLogin(SocialLoginView):
#     adapter_class = google_view.GoogleOAuth2Adapter
#     callback_url = GOOGLE_CALLBACK_URI
#     client_class = OAuth2Client


### 유저 관련
class UserInfoView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        responses= {
            200: 'Success',
            401: '권한 없음'
        })
    def get(self, request):
        '''
            ## 유저 정보 조회
            `
            "id": 2,
            "username": "이름",
            "email": "pse314@gmail.com",
            "date_joined": "2023-08-04T11:59:59.753534+09:00",
            "profile_img": null,
            "fighting": 5,
            "resol_msg": "아자아자 파이팅",
            "user_tags": [ "tag1", "tag2" ],
            "user_regions": [ "관심지역3" ]
            `
        '''
        user_info = get_userinfo(request.user)
        res = ResponseDto(status=200, data=user_info, msg=message["UserInfoGetSuccess"])
        return responseFactory(res)

class UsernameView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DefaultSerializer

    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        responses= {
            200: 'Success',
            401: '권한 없음'
        })
    def put(self, request):
        '''
            ## 유저네임 변경
        '''
        res = update_username(request)
        return responseFactory(res)


class ResolMsgView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DefaultSerializer
    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        responses= {
            200: 'Success',
            401: '권한 없음'
        })
    def put(self, request):
        '''
            ## 유저 다짐메세지 변경
        '''
        res = update_resol_msg(request)
        return responseFactory(res)


class FightingView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DefaultSerializer

    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        responses= {
            200: 'Success',
            401: '권한 없음'
        })
    def post(self, request):
        '''
            ## 로그인한 유저의 파이팅 1점 올리기
        '''
        user = request.user
        res = inc_fighting(user)
        return responseFactory(res)


### 유저 태그/지역 관련
class UserTagView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserTagListSerializer
    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        responses= {
            200: 'Success',
            400: 'bad request, 또는 태그 수가 1개 미만/10개 초과',
            401: '권한 없음'
        })
    def post(self, request):
        '''
            ## 유저 태그 수정
            - tags: 리스트 형식의 태그
            Ex. `"tags": ["tag1", "tag2"]`
            - 태그가 1개 미만, 10개 초과인 경우 400 에러 발생
        '''
        res = update_user_tags(request.user, request.data)
        return responseFactory(res)

class UserRegionView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRegionListSerializer
    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        responses= {
            200: 'Success',
            400: 'bad request, 또는 지역 수가 1개 미만/10개 초과',
            401: '권한 없음'
        })
    def post(self, request):
        '''
            ## 유저 지역 수정
            - regions: 리스트 형식의 지역
            Ex. `"regions": ["region1", "region2"]`
            - 지역이 1개 미만, 10개 초과인 경우 400 에러 발생
        '''
        res = update_user_region(request.user, request.data)
        return responseFactory(res)