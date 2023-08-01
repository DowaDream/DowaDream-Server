from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings

# 구글 소셜로그인 변수 설정
BASE_URL = settings.BASE_URL
CLIENT_URL = "https://www.google.com/"  # 임시로 redirect할 URL
GOOGLE_CALLBACK_URI = BASE_URL + 'user/callback/'

# 구글 로그인
def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email "
    client_id = settings.GOOGLE_CLIENT_ID
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


from json import JSONDecodeError
from django.http import JsonResponse
import requests
from .models import *
from allauth.socialaccount.models import SocialAccount
from rest_framework import status

# Callback 함수
def google_callback(request):
    client_id = settings.GOOGLE_CLIENT_ID
    client_secret = settings.GOOGLE_PASSWORD
    code = request.GET.get('code')
    state = "random_state"

    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get('access_token')

    # 가져온 access_token으로 이메일값을 구글에 요청
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 성공 시 이메일 가져오기
    email_req_json = email_req.json()
    email = email_req_json.get('email')

    # 이메일, access_token, code를 바탕으로 회원가입/로그인
    try:
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

        # 이미 Google로 제대로 가입된 유저 => 로그인
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}user/login/finish/", data=data)
        accept_status = accept.status_code

        # 문제가 생기면 에러
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)
        return redirect("https://www.google.com/")
    

    except User.DoesNotExist:
        # 회원가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}user/login/finish/", data=data)
        accept_status = accept.status_code

        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)
        return redirect("https://www.google.com/")


from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google import views as google_view

class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client