import requests
from django.conf import settings
from .response import *
from .jwt_token import make_token
from django.http import JsonResponse
from user.models import User
from json import JSONDecodeError
from .serializers import *

BASE_URL = settings.BASE_URL
GOOGLE_CALLBACK_URI = BASE_URL + 'user/callback/'


### 구글 로그인 관련 ###
def get_google_access_token(code):
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

def get_google_profile(access_token):
    # 가져온 access_token으로 사용자 정보를 구글에 요청
    profile_req = requests.get(f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}")
    profile_req_status = profile_req.status_code
    if profile_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get profile'}, status=400)
    
    # 성공 시 프로필 정보 가져오기
    profile_req_json = profile_req.json()
    email = profile_req_json.get('email')
    profile_picture = profile_req_json.get('picture')  # 프로필 사진 URL
    return email, profile_picture


# 로그인
def google_callback_signin(data, user, email) -> ResponseDto:
    accept = requests.post(f"{BASE_URL}user/login/finish/", data=data)
    accept_status = accept.status_code

    # 로그인 과정에서 문제가 생기면 에러
    if accept_status != 200:
        return ResponseDto(status=accept_status, msg=message['SignInFail'])
    
    data = make_token(email, accept, user)
    return ResponseDto(status=200, msg=message['SignInSuccess'], data=data)


# 회원가입
def google_callback_signup(data, email, profile_img) -> ResponseDto:
    accept = requests.post(f"{BASE_URL}user/login/finish/", data=data)
    accept_status = accept.status_code

    if accept_status != 200:
        return ResponseDto(status=accept_status, msg=message['SignUpFail'])

    user = User.objects.get(email=email)
    user.profile_img = profile_img  # profile_img 저장
    user.save()  # 변경 내용을 저장
    data = make_token(email, accept, user)
    return ResponseDto(status=201, msg=message['SignUpSuccess'], data=data)



### 유저 관련 ###
def update_username(request):
    new_name = request.data.get('username')
    if new_name:
        user = request.user  # 현재 로그인된 사용자
        user.username = new_name
        user.save()
        return ResponseDto(status=200, msg=message['UsernamePutSuccess'])
    else:
        return ResponseDto(status=400, msg=message['UsernameIsEmpty'])

def update_resol_msg(request) -> ResponseDto:
    resol_msg = request.data.get('resol_msg')
    if resol_msg:
        user = request.user
        user.resol_msg = resol_msg
        user.save()
        return ResponseDto(status=200, msg=message['ResolMsgPutSuccess'])
    else:
        return ResponseDto(status=400, msg=message['ResolMsgIsEmpty'])

def inc_fighting(user) -> ResponseDto:
    user.fighting += 1
    user.save()
    return ResponseDto(status=200, msg=message['IncreasedFighting'])


def update_user_tags(user, data) -> ResponseDto:
    tags = data.get('tags')
    serializer = UserTagSerializer(data=data)
    if not serializer.is_valid():
        return ResponseDto(status=400, msg=serializer.errors)
    User_Tag.objects.filter(user=user).delete() # 기존의 태그 삭제
    created_tags = []
    for tag in tags:
        created_tag = User_Tag.objects.create(user=user, tag=tag)
        created_tags.append(created_tag.tag)
    return ResponseDto(status=200, data=created_tags, msg=message['CreatedUserTags'])

def update_user_region(user, data) -> ResponseDto:
    regions = data.get('regions')
    serializer = UserRegionSerializer(data=data)
    if not serializer.is_valid():
        return ResponseDto(status=400, msg=serializer.errors)
    User_Region.objects.filter(user=user).delete() # 기존의 지역 삭제
    created_regions = []
    for region in regions:
        created_region = User_Region.objects.create(user=user, region=region)
        created_regions.append(created_region.region)
    return ResponseDto(status=200, data=created_regions, msg=message['CreatedUserRegion'])