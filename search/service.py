import requests
import xmltodict
from django.conf import settings



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
            title = items['progrmSj']
            place = items['actPlace']
            progrmRegistNo = items['progrmRegistNo']

            temp['title'] = title
            temp['place'] = place
            temp['progrmRegistNo'] = progrmRegistNo
            result.append(temp)
        # print(items)
        else:
            for item in items:
                temp = {}
                title = item.get('progrmSj')
                place = item.get('actPlace')
                progrmRegistNo = item.get('progrmRegistNo')

                temp['title'] = title
                temp['place'] = place
                temp['progrmRegistNo'] = progrmRegistNo
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
        print(f"actStartDate: {actStartDate}, actStartTime: {actStartTime}")
        actEndDate = item.get('progrmEndde')
        actEndTime = item.get('actEndTm')
        print(f"actEndDate: {actEndDate}, actEndTime: {actEndTime}")
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
