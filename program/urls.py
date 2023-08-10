from django.urls import path
from .views import *

urlpatterns = [
    path('', PrgmInteractUpdateView.as_view()),
]