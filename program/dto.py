from datetime import datetime


class ProgramDto:
    def __init__(self, tagName, title, registerInstitute, recruitStart, recruitEnd, actStart, actEnd):
        self.tag = tagName.split()[0]
        self.title = title  # 봉사 제목
        self.registerInstitute = registerInstitute  # 등록 기관
        self.recruitStart = recruitStart    # 모집 시작일
        self.recruitEnd = recruitEnd    # 모집 종료일
        self.actStart = actStart    # 봉사 시작일
        self.actEnd = actEnd    # 봉사 종료일
        self.dday = self.calculate_d_day(recruitEnd)    # 디데이
    
    def calculate_d_day(self, date):
        try:
            date = datetime.strptime(date, '%Y/%m/%d')  # 문자열을 파싱하여 datetime 객체로 변환
            today = datetime.now()
            d_day = (date - today).days
            return d_day
        except ValueError:
            # 날짜 문자열 파싱 오류 처리
            return None
    
    
    def to_json(self):
        return {
            "tag": self.tag,
            "title": self.title,
            "registerInstitute": self.registerInstitute,
            "recruitStart": self.recruitStart,
            "recruitEnd": self.recruitEnd,
            "actStart": self.actStart,
            "actEnd": self.actEnd,
            "dday": self.dday
        }