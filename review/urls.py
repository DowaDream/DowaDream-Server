from django.urls import path
from .views import *

urlpatterns = [
    path('', UserReviewList.as_view()),
    path('user/', get_user_reviews),    # 사용자가 쓴 리뷰 반환
    path('cheer/', ReviewCheerGetView.as_view()),
    
    path('<int:rid>/', UserReviewDetail.as_view()),
    path('<int:rid>/comment/', CommentList.as_view()),
    path('<int:rid>/comment/<int:cid>/', CommentDetail.as_view()),
    path('<int:rid>/cheer/', ReviewCheerView.as_view()),
    
    path('user/', AuthenticatedUserGetList.as_view()),
]