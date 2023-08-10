from django.urls import path
from .views import *

urlpatterns = [
    path('', PrgmInteractUpdateView.as_view()),
    
    path('cheered/', CheeredGetView.as_view()),
    path('participated/', ParticipatedGetView.as_view()),
    path('clipped/', ClippedGetView.as_view()),
]