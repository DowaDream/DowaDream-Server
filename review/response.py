def ReviewCreateSuccessed(data):
    return {
        'status': 201,
        'message': '리뷰 생성 성공',
        'data': data
    }

def ReviewCreateFailed(err):
    return {
        'status': 400,
        'message': '리뷰 생성 실패',
        'err_message': err
    }

def ReviewImageFormatError(err):
    return {
        'status': 400,
        'message': '이미지 오류(jpg, jpeg, png, gif만 가능',
        'err_message': err
    }

def ReviewImageUploadError():
    return {
        'status': 500,
        'message': '이미지 s3 업로드 중 오류',
    }