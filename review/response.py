from typing import Union

class ResponseDto:
    def __init__(self, status, msg, data=None):
        self.status = status
        self.data = data
        self.msg = msg


message = {
    # 리뷰 관련
    "TooManyImages": "이미지는 최대 5장까지 가능",
    "ImageFormatError": "이미지 파일 저장 불가",
    "ReviewCreateSuccess": "리뷰 생성 성공",
    "ReviewPutSuccess": "리뷰 수정 성공",
    
    "ReviewListGetSuccess": "리뷰 리스트 조회 성공",
    "ReviewGetSuccess": "단일 리뷰 조회 성공",
    "ReviewNotFound": "일치하는 리뷰 없음",
    
    "ReviewDeleteSuccess": "리뷰 삭제 성공",
    "ReviewDeleteFailed": "리뷰 삭제 실패",
    
    
    # 댓글 관련
    "CommentGetSuccess": "댓글 조회 성공",
    "CommentCreateSuccess": "댓글 생성 성공",
    "CommentPutSuccess": "댓글 수정 성공",
    "CommentDeleteSuccess": "댓글 삭제 성공",
    
    "InvalidFormat": "올바르지 않은 형식",
    
}