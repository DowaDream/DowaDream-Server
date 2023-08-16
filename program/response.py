
class ResponseDto:
    def __init__(self, status, msg, data=None):
        self.status = status
        self.data = data
        self.msg = msg


message = {
    "PrgmInteractSuccess": "봉사내역/스크랩/응원하기 상태 업데이트 성공",
    "PrgmInteractFail": "봉사내역/스크랩/응원하기 상태 업데이트 실패",
    
    "CheeredGetSuccess": "응원한 봉사 리스트 조회 성공",
    "ParticipatedGetSuccess": "참여한 봉사 리스트 조회 성공",
    "ClippedGetSuccess": "스크랩한 봉사 리스트 조회 성공",
    
}

def searchResponseFactory(result):
    code = 200
    msg = 'OK'
    if result is None:
        code = '404'
        msg = 'Not Found'
    return {
            'status': code,
            'message': msg,
            'data': result
        }