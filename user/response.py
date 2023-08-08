
class ResponseDto:
    def __init__(self, status, msg, data=None):
        self.status = status
        self.data = data
        self.msg = msg


message = {
    # 로그인/회원가입 관련
    "SignInSuccess": "로그인 성공",
    "SignInFail": "로그인 실패",
    "SignUpSuccess": "회원가입 성공",
    "SignUpFail": "회원가입 실패",
    
    "UsernamePutSuccess": "유저네임 수정 성공",
    "UsernameIsEmpty": "유저네임이 비었음",
    "ResolMsgPutSuccess": "다짐 메세지 수정 성공",
    "ResolMsgIsEmpty": "다짐 메세지가 비었음",
    
}