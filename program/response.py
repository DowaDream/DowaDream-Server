
class ResponseDto:
    def __init__(self, status, msg, data=None):
        self.status = status
        self.data = data
        self.msg = msg


message = {
    "PrgmInteractSuccess": "봉사내역/스크랩/응원하기 상태 업데이트 성공",
    "PrgmInteractFail": "봉사내역/스크랩/응원하기 상태 업데이트 실패",
}