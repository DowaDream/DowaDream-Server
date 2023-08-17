from rest_framework_simplejwt.serializers import RefreshToken


def make_token(email, user):
    # accept_json = accept.json()
    # accept_json.pop('user', None)
    token = RefreshToken.for_user(user)
    refresh_token = str(token)
    access_token = str(token.access_token)
    data = {
	    'email': email,
	    'refresh_token':refresh_token,
	    'access_token':access_token,
    }
    
    return data