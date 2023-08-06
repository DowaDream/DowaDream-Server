def SignInSuccessed(data):
    return {
        'status': 200,
        'message': '로그인 성공',
        'data': data
    }

def SignInFailed(status):
    return {
        'err_msg': '로그인 실패',
        'status': status
    }

def SignUpSuccess(data):
    return {
        'status': 201,
        'message': '회원가입 성공',
        'data': data
    }

def SignUpFailed(status):
    return {
        'err_msg': '회원가입 실패',
        'status': status
    }
