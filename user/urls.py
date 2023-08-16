from django.urls import path
from .views import *

urlpatterns = [
    path('login/', google_login, name='google_login'),
    path('callback/', google_callback, name='google_callback'),
    path('login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
    
    path('info/', UserInfoView.as_view()),
    path('resol/', ResolMsgView.as_view()),
    path('username/', UsernameView.as_view()),
    path('fighting/', FightingView.as_view()),
    
    path('tag/', UserTagView.as_view()),
    path('region/', UserRegionView.as_view()),
]