from django.urls import path
from .views import *

urlpatterns = [
    path('', ReviewList.as_view()),
    path('<int:rid>/', ReviewDetail.as_view()),
    
    path('<int:rid>/comment/', CommentList.as_view()),
    path('<int:rid>/comment/<int:cid>/', CommentDetail.as_view()),
]