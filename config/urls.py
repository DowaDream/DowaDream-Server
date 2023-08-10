from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('search/', include('search.urls')),
  
    path('user/', include('user.urls')),
    path('user/', include('dj_rest_auth.urls')),
    path('user/', include('allauth.urls')),
    
    path('review/', include('review.urls')),
    path('program/', include('program.urls'))
]