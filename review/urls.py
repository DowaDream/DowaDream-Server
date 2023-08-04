from django.urls import path
from .views import *

urlpatterns = [
    path('', ReviewList.as_view()),
    path('<int:rid>/', ReviewDetail.as_view())
    
]