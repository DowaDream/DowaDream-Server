from django.urls import path
from .views import *

urlpatterns = [
    path('keyword/', SearchKeywordView.as_view(), name='search_keyword'),
    path('area/', SearchAreaView.as_view(), name='search_area'),
    path('registno/', SearchRegistNoView.as_view(), name='search_regist_no'),
]