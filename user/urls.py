from django.urls import path
from .views import *

urlpatterns = [
    path('login/', google_login, name='google_login'),
    path('callback/', google_callback, name='google_callback'),
    path('login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
    
    path('token/', JWTView.as_view(), name='create_jwt_token'),
]