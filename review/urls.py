from django.urls import path
from .views import *

urlpatterns = [
    path('', UserReviewList.as_view()),
    path('user/', AuthenticatedUserGetList.as_view()),
    path('user/cheer/', ReviewCheerGetView.as_view()),
    path('user/cheer/<int:rid>/', ReviewCheerView.as_view()),
    
    path('<int:rid>/', UserReviewDetail.as_view()),
    path('<int:rid>/comment/', CommentList.as_view()),
    path('<int:rid>/comment/<int:cid>/', CommentDetail.as_view()),
]