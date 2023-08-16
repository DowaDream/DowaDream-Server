import json
from datetime import datetime

import requests
import xmltodict
from django.conf import settings
from django.http import JsonResponse
from user.models import User

from .response import *
from .models import *
from .serializers import *
from .dto import ProgramDto
from .search_service import *


def update_progrm_interact(data, user) -> ResponseDto:
    progrmRegistNo = data.get('progrmRegistNo')
    
    try:
        interact = Program_Interaction.objects.get(progrmRegistNo=progrmRegistNo, user=user)
    
    except Program_Interaction.DoesNotExist:
        # 해당하는 progrmRegistNo가 없으면 새로운 튜플 생성
        interact = Program_Interaction(progrmRegistNo=progrmRegistNo, user=user)
    
    # request body에서 해당 필드의 값을 가져오고, 필드 값이 없으면 기존값을 넣음
    cheered = data.get('cheered', interact.cheered)
    participated = data.get('participated', interact.participated)
    clipped = data.get('clipped', interact.clipped)
    
    # 필드 값 설정
    interact.cheered = cheered
    interact.participated = participated
    interact.clipped = clipped
    interact.user = user
    
    serializer = PrgmInteractSerializer(interact, data=data)
    if serializer.is_valid():
        serializer.save()
        return ResponseDto(status=200, data=serializer.data, msg=message['PrgmInteractSuccess'])
    
    return ResponseDto(status=400, data=serializer.errors, msg=message['PrgmInteractFail'])


def get_interactions_list(user, field_name):
    interactions = Program_Interaction.objects.filter(user=user, **{field_name: True})
    interations_list = list(interactions.values_list('progrmRegistNo', flat=True))  # flat=False: value 하나를 list로 저장
    return interations_list



def get_cheer_recommend():
    interactions = Program_Interaction.objects.filter(cheered=True).annotate(cheer_count=Count('cheered')).order_by('-cheer_count')
    progrmList = list(interactions.values_list('progrmRegistNo', flat=True))
    
    data = []
    for program in progrmList[:4]:
        p_data = callByRegistNo(program)
        program_dto_data = ProgramDto(tagName=p_data['tagName'], title=p_data['title'], registerInstitute=p_data['registerInstitute'], \
                                        recruitStart=p_data['recruitStart'], recruitEnd=p_data['recruitEnd'], actStart=p_data['actStart'], actEnd=p_data['actEnd'])
        data.append(program_dto_data.to_json())
    return ResponseDto(status=200, data=data, msg=message['PrgrmRecommendCheer'])


    return None
def findTagCode(tagName):
    # split tagname by ' > '
    tagNameHigh = tagName.split(' > ')[0]
    # find tagCodeHigh from tagList.json
    with open(CURRENT_PATH / 'tagList.json', 'r', encoding='utf-8') as f:
        tagList = json.load(f)
    for tag in tagList:
        if tag['hignClsNm'] == tagNameHigh and tag['lowClsNm'] == tagNameLow:
            tagCodeHigh = tag['highClsCd']
            tagCodeLow = tag['lowClsCd']
            return tagCodeLow
    tagNameLow = tagName.split(' > ')[1]



def callByKeyword(keyword, actPlace=None):
    url = 'http://openapi.1365.go.kr/openapi/service/rest/VolunteerPartcptnService/getVltrSearchWordList'
    params = {
        'keyword' : keyword,
        'schCateGu' : 'all',
        'actPlace' : actPlace
        }
    response = requests.get(url, params=params)
    parsed_xml = xmltodict.parse(response.text)

    # myjson = json.dumps(parsed_xml,ensure_ascii = False)
    # print(myjson)

    if parsed_xml["response"]["header"]["resultCode"] == "00":
        result = []
        itemsList = parsed_xml["response"]["body"]["items"]
        if itemsList is None:
            return None
        items = itemsList['item']
        # 게시물이 여러개일 때는 items가 list인데, 하나일 때는 dict이기 때문에 분기를 나누어 처리
        if type(items) is dict:
            temp = {}
            temp['title'] = items['progrmSj']
            temp['place'] = items['actPlace']
            temp['progrmRegistNo'] = items['progrmRegistNo']

            result.append(temp)
        # print(items)
        else:
            for item in items:
                temp = {}
                temp['title'] = item.get('progrmSj')
                temp['place'] = item.get('actPlace')
                temp['progrmRegistNo'] = item.get('progrmRegistNo')

                result.append(temp)
        # print(result)
        return result
    else:
        return None

def callByArea(keyword):
    url = 'http://openapi.1365.go.kr/openapi/service/rest/VolunteerPartcptnService/getVltrAreaList'
    params = {
    'serviceKey' : settings.VOL_API_KEY,
    'schCateGu' : 'all',
    'schSign1' : keyword, # 지역코드 (구군)    
    }
    # 시도 단위로 검색하려면, schSign1 대신
    # 'schSido' : keyword # 지역코드(시도)


    response = requests.get(url, params=params)
    parsed_xml = xmltodict.parse(response.text)
    # myjson = json.dumps(parsed_xml,ensure_ascii = False)
    # print(myjson)
    if parsed_xml["response"]["header"]["resultCode"] == "00":
        result = []
        itemsList = parsed_xml["response"]["body"]["items"]
        if itemsList is None:
            return None
        items = itemsList['item']
        if type(items) is dict:
            temp = {}
            temp['title'] = items['progrmSj']
            temp['progrmRegistNo'] = items['progrmRegistNo']
            result.append(temp)

        for item in items:
            temp = {}
            title = item.get('progrmSj')
            # 놀랍게도 장소 정보를 제공하지 않아, 등록번호로 검색해야 한다
            # 하지만 API call 개수가 너무 많으면 로딩이 느려지므로 일단은 장소 정보 없이 제공
            # 향후 필요할 경우 callByRegistNo 함수를 이용해 장소 정보를 가져옴
            progrmRegistNo = item.get('progrmRegistNo')

            temp['title'] = title
            temp['progrmRegistNo'] = progrmRegistNo
            result.append(temp)
        return result
    else:
        return None

def callByRegistNo(registNo):
    url = 'http://openapi.1365.go.kr/openapi/service/rest/VolunteerPartcptnService/getVltrPartcptnItem'
    params ={
        'serviceKey' : settings.VOL_API_KEY,
        'progrmRegistNo' : registNo
    }
    response = requests.get(url, params=params)
    parsed_xml = xmltodict.parse(response.text)
    # myjson = json.dumps(parsed_xml,ensure_ascii = False)
    # print(myjson)

    # print(list(parsed_xml['response'].keys()))

    if parsed_xml["response"]["header"]["resultCode"] == "00":
        tempVarForNoneCheck = parsed_xml["response"]["body"]["items"]
        if tempVarForNoneCheck is None:
            return None
        item = tempVarForNoneCheck["item"]

        temp = {}

        # 날짜와 시간 값 먼저 처리하기
        actStartDate = item.get('progrmBgnde')
        actStartTime = item.get('actBeginTm')
        # print(f"actStartDate: {actStartDate}, actStartTime: {actStartTime}")
        actEndDate = item.get('progrmEndde')
        actEndTime = item.get('actEndTm')
        # print(f"actEndDate: {actEndDate}, actEndTime: {actEndTime}")
        actStart = actStartDate[0:4] + '/' + actStartDate[4:6] + '/' + actStartDate[6:8] + '-' + actStartTime + ':00:00'
        actEnd = actEndDate[0:4] + '/' + actEndDate[4:6] + '/' + actEndDate[6:8] + '-' + actEndTime + ':00:00'
        tempRecruitStart = item.get('noticeBgnde')
        tempRecruitEnd = item.get('noticeEndde')
        recruitStart = tempRecruitStart[0:4] + '/' + tempRecruitStart[4:6] + '/' + tempRecruitStart[6:8]
        recruitEnd = tempRecruitEnd[0:4] + '/' + tempRecruitEnd[4:6] + '/' + tempRecruitEnd[6:8]

        # 값 가져오기
        temp['title'] = item.get('progrmSj')
        temp['recruitStatusNm'] = item.get('progrmSttusSe')
        temp['actStart'] = actStart
        temp['actEnd'] = actEnd
        temp['place'] = item.get('actPlace')
        temp['adultAble'] = item.get('adultPosblAt')
        temp['teenAble'] = item.get('yngbgsPosblAt')
        temp['recruitStart'] = recruitStart
        temp['recruitEnd'] = recruitEnd
        temp['recruitInstitute'] = item.get('mnnstNm')
        temp['registerInstiute'] = item.get('nanmmbyNm')
        temp['maxPerson'] = item.get('rcritNmpr')
        temp['content']= item.get('progrmCn')
        temp['progrmRegistNo'] = registNo

        return temp
    else:
        return None

