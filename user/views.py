from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google import views as google_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .service import *
from .models import *
from .response import *


def responseFactory(res: ResponseDto):
    if res.data is None:
        return JsonResponse(status=res.status, data={ "msg": res.msg })
    else:
        return JsonResponse(
            status=res.status,
            data={ "msg": res.msg, "data": res.data }
        )



# 구글 로그인
def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email "
    client_id = settings.GOOGLE_CLIENT_ID
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


# Callback 함수
def google_callback(request):
    code = request.GET.get('code')
    access_token = get_google_access_token(code)
    email, profile_img = get_google_profile(access_token)

    try:
        user = User.objects.get(email=email)

        # 이미 Google로 제대로 가입된 유저 => 로그인
        data = {'access_token': access_token, 'code': code}
        res = google_callback_signin(data, user, email)
        return responseFactory(res)

    except User.DoesNotExist:   # 회원가입
        data = {'access_token': access_token, 'code': code}
        res = google_callback_signup(data, email, profile_img)
        return responseFactory(res)


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_username(request):
    new_name = request.data.get('username')
    if new_name:
        user = request.user  # 현재 로그인된 사용자
        user.username = new_name
        user.save()
        res = ResponseDto(status=200, msg=message['UsernamePutSuccess'])
    else:
        res = ResponseDto(status=400, msg=message['UsernameIsEmpty'])
    return responseFactory(res)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_resol_msg(request):
    resol_msg = request.data.get('resol_msg')
    if resol_msg:
        user = request.user
        user.resol_msg = resol_msg
        user.save()
        res = ResponseDto(status=200, msg=message['ResolMsgPutSuccess'])
    else:
        res = ResponseDto(status=400, msg=message['ResolMsgIsEmpty'])
    return responseFactory(res)