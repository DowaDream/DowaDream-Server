from django.urls import path
from .views import *

urlpatterns = [
    path('', ReviewList.as_view())
    # path('login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
]