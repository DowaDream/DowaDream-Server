### 생성 관련 Response
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




### Review Detail 관련 Response
def ReviewDetailGetSuccess(data):
    return {
        'status': 200,
        'message': '리뷰 Detail 조회 성공',
        'data': data
    }

def ReviewPutSuccess(data):
    return {
        'status': 200,
        'message': '리뷰 수정 성공',
        'data': data
    }

def ReviewPutFailed(err):
    return {
        'status': 400,
        'message': '형식이 맞지 않음',
        'error_message': err
    }

def ReviewDeleteSuccess(rid):
    return {
        'status': 204,
        'message': '리뷰 삭제 성공',
        'rid': rid
    }