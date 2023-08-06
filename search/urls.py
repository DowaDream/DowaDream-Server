from django.urls import path
from .views import *

urlpatterns = [
    path('keyword/', search_keyword, name='search_keyword'),
    path('area/', search_area, name='search_area'),
    path('registno/', search_regist_no, name='search_regist_no'),
]