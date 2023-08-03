import requests
from django.conf import settings
from .response import *
from .jwt_token import make_token
from django.http import JsonResponse
from user.models import User
from json import JSONDecodeError

BASE_URL = settings.BASE_URL
GOOGLE_CALLBACK_URI = BASE_URL + 'user/callback/'

def get_google_access_token(request, code):
    client_id = settings.GOOGLE_CLIENT_ID
    client_secret = settings.GOOGLE_PASSWORD
    state = "random_state"

    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    if error is not None:
        raise JSONDecodeError(error)
    
    access_token = token_req_json.get('access_token')
    return access_token


def get_google_email(access_token):
    # 가져온 access_token으로 이메일값을 구글에 요청
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=400)
    
    # 성공 시 이메일 가져오기
    email_req_json = email_req.json()
    email = email_req_json.get('email')
    return email


# 로그인
def google_callback_signin(data, user, email):
    accept = requests.post(f"{BASE_URL}user/login/finish/", data=data)
    accept_status = accept.status_code

    # 로그인 과정에서 문제가 생기면 에러
    if accept_status != 200:
        return SignInFailed(accept_status)
    
    data = make_token(email, accept, user)
    return SignInSuccessed(data)


# 회원가입
def google_callback_signup(data, email):
    accept = requests.post(f"{BASE_URL}user/login/finish/", data=data)
    accept_status = accept.status_code

    if accept_status != 200:
        return SignUpFailed(accept_status)

    user = User.objects.get(email=email)
    data = make_token(email, accept, user)
    return SignUpSuccess(data)