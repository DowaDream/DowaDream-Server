import requests
import xmltodict
from django.conf import settings
from datetime import datetime, timedelta
import json

from pathlib import Path
CURRENT_PATH = Path(__file__).parent.absolute()

def findTagCode(tagName):
    # split tagname by ' > '
    tagNameHigh = tagName.split(' > ')[0]
    tagNameLow = tagName.split(' > ')[1]
    # find tagCodeHigh from tagList.json
    with open(CURRENT_PATH / 'tagList.json', 'r', encoding='utf-8') as f:
        tagList = json.load(f)
    for tag in tagList:
        if tag['hignClsNm'] == tagNameHigh and tag['lowClsNm'] == tagNameLow:
            tagCodeHigh = tag['highClsCd']
            tagCodeLow = tag['lowClsCd']
            return tagCodeHigh
    return None

def callByKeyword(keyword, actPlace=None, tagCode=None, areaCode=None):
    url = 'http://openapi.1365.go.kr/openapi/service/rest/VolunteerPartcptnService/getVltrSearchWordList'
    
    params = {
        'keyword' : keyword,
        'schCateGu' : 'all',
        'actPlace' : actPlace,
        'schSign1' : areaCode,
        'upperClCode' : tagCode,
        'numOfRows' : 50
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
        for item in items:
            temp = {}
            temp['title'] = item.get('progrmSj')
            temp['place'] = item.get('actPlace')
            temp['progrmRegistNo'] = item.get('progrmRegistNo')
            temp['tagCode'] = tagCode
            temp['areaCode'] = areaCode
            temp['recruitInstitute'] = item.get('nanmmbyNm')
            temp['url'] = item.get('url')

            # yyyymmdd -> yyyy/mm/dd
            unparsedRecStartDate = item.get('noticeBgnde')
            temp['recruitStart'] = unparsedRecStartDate[0:4] + '/' + unparsedRecStartDate[4:6] + '/' + unparsedRecStartDate[6:8]
            unparsedRecEndDate = item.get('noticeEndde')
            temp['recruitEnd'] = unparsedRecEndDate[0:4] + '/' + unparsedRecEndDate[4:6] + '/' + unparsedRecEndDate[6:8]

            # yyyymmdd -> yyyy/mm/dd-hh:mm:ss
            unparsedActStartDate = item.get('progrmBgnde')
            unparsedActStartTime = item.get('actBeginTm')
            # if unparsedActStartTime is smaller than 10, add 0
            if int(unparsedActStartTime) < 10:
                unparsedActStartTime = '0' + unparsedActStartTime
            temp['actStart'] = unparsedActStartDate[0:4] + '/' + unparsedActStartDate[4:6] + '/' + unparsedActStartDate[6:8] + '-' + unparsedActStartTime + ':00:00'
            unparsedActEndDate = item.get('progrmEndde')
            unparsedActEndTime = item.get('actEndTm')
            temp['actEnd'] = unparsedActEndDate[0:4] + '/' + unparsedActEndDate[4:6] + '/'+ unparsedActEndDate[6:8] + '-' + unparsedActEndTime + ':00:00'

            # d-day 계산 -> recruitEnd - today
            temp['dday'] = (datetime.strptime(temp['recruitEnd'], '%Y/%m/%d') - datetime.today()).days

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
        'schSign1' : keyword, # 지역코드 (구군),
        'numOfRows' : 50    
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
        'progrmRegistNo' : registNo,
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
        temp['registerInstitute'] = item.get('nanmmbyNm')
        temp['maxPerson'] = item.get('rcritNmpr')
        temp['content']= item.get('progrmCn')
        temp['progrmRegistNo'] = registNo
        temp['tagName'] = item.get('srvcClCode')
        temp['url'] = f"https://www.1365.go.kr/vols/P9210/partcptn/timeCptn.do?type=show&progrmRegistNo={registNo}"
        temp['areaCode'] = item.get('gugunCd')
        temp['tagCode'] = findTagCode(temp['tagName'])

        return temp
    else:
        return None

def callByDday():
    url = 'http://openapi.1365.go.kr/openapi/service/rest/VolunteerPartcptnService/getVltrSearchWordList'

    # convert to string, yyyymmdd
    today = datetime.today().strftime('%Y%m%d')

    result = []
    while len(result) < 10:
        params ={
            'noticeEndde' : today,
        }
        response = requests.get(url, params=params)
        parsed_xml = xmltodict.parse(response.text)


        if parsed_xml["response"]["header"]["resultCode"] == "00":
            itemsList = parsed_xml["response"]["body"]["items"]
            if itemsList is None:
                return None
            items = itemsList['item']
            for item in items:
                temp = {}
                temp['title'] = item.get('progrmSj')
                temp['place'] = item.get('actPlace')
                temp['progrmRegistNo'] = item.get('progrmRegistNo')
                temp['recruitInstitute'] = item.get('nanmmbyNm')
                temp['url'] = item.get('url')

                # yyyymmdd -> yyyy/mm/dd
                unparsedRecStartDate = item.get('noticeBgnde')
                temp['recruitStart'] = unparsedRecStartDate[0:4] + '/' + unparsedRecStartDate[4:6] + '/' + unparsedRecStartDate[6:8]
                unparsedRecEndDate = item.get('noticeEndde')
                temp['recruitEnd'] = unparsedRecEndDate[0:4] + '/' + unparsedRecEndDate[4:6] + '/' + unparsedRecEndDate[6:8]

                # yyyymmdd -> yyyy/mm/dd-hh:mm:ss
                unparsedActStartDate = item.get('progrmBgnde')
                unparsedActStartTime = item.get('actBeginTm')
                # if unparsedActStartTime is smaller than 10, add 0
                if int(unparsedActStartTime) < 10:
                    unparsedActStartTime = '0' + unparsedActStartTime
                temp['actStart'] = unparsedActStartDate[0:4] + '/' + unparsedActStartDate[4:6] + '/' + unparsedActStartDate[6:8] + '-' + unparsedActStartTime + ':00:00'
                unparsedActEndDate = item.get('progrmEndde')
                unparsedActEndTime = item.get('actEndTm')
                temp['actEnd'] = unparsedActEndDate[0:4] + '/' + unparsedActEndDate[4:6] + '/'+ unparsedActEndDate[6:8] + '-' + unparsedActEndTime + ':00:00'

                # d-day 계산 -> recruitEnd - today
                temp['dday'] = (datetime.strptime(temp['recruitEnd'], '%Y/%m/%d') - datetime.today()).days
                result.append(temp)
    if result is None:
        return None
    return result