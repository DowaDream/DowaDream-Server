from django.urls import path
from .views import *

urlpatterns = [
    path('', PrgmInteractUpdateView.as_view()),
    
    path('recommend/cheer/', PrgmRecommendCheeringView.as_view()),
    
    path('cheered/', CheeredGetView.as_view()),
    path('participated/', ParticipatedGetView.as_view()),
    path('clipped/', ClippedGetView.as_view()),
    path('search/keyword/', SearchKeywordView.as_view(), name='search_keyword'),
    path('search/area/', SearchAreaView.as_view(), name='search_area'),
    path('search/registno/', SearchRegistNoView.as_view(), name='search_regist_no'),
]