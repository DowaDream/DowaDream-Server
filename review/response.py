### Review 생성 관련 Response
def ReviewCreateSuccessed(data):
    return {
        'status': 201,
        'message': '리뷰 생성 성공',
        'data': data
    }

def ReviewFailed(err):
    return {
        'status': 400,
        'err_message': err
    }

def ReviewImageFormatError(err):
    return {
        'status': 400,
        'message': '이미지 파일 오류',
        'err_message': err
    }

def ReviewImageUploadError():
    return {
        'status': 500,
        'message': '이미지 s3 업로드 중 오류',
    }

def ReviewTooManyImages():
    return {
        'status': 400,
        'message': '이미지는 최대 5장까지 가능'
    }

def ReviewGetListSuccess(data):
    return {
        'status': 200,
        'message': '리뷰 리스트 조회 성공',
        'data': data
    }

def ReviewGetListFail():
    return {
        'status': 500,
        'message': '리뷰 리스트 조회 실패',
    }



### Review Detail 관련 Response
def ReviewDetailGetSuccess(data):
    return {
        'status': 200,
        'message': '리뷰 Detail 조회 성공',
        'data': data
    }

def ReviewDetailGetFail():
    return {
        'status': 500,
        'message': '리뷰 Detail 조회 실패',
    }

def ReviewPutSuccess(data):
    return {
        'status': 200,
        'message': '리뷰 수정 성공',
        'data': data
    }

def ReviewDeleteSuccess(rid):
    return {
        'status': 204,
        'message': '리뷰 삭제 성공',
        'rid': rid
    }

def ReviewDeleteFail(rid):
    return {
        'status': 500,
        'message': '리뷰 삭제 실패',
        'rid': rid
    }


### Comment 관련 Response
def CommentGetSuccess(data):
    return {
        'status': 200,
        'message': '댓글 조회 성공',
        'data': data
    }

def CommentCreateSuccess(data):
    return {
        'status': 201,
        'message': '댓글 생성 성공',
        'data': data
    }

def CommentCreateFail(err):
    return {
        'status': 400,
        'message': '댓글 생성 실패',
        'error_message': err
    }