from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view( 
    openapi.Info( 
        title="Dowadream API", 
        default_version="v1", 
        description="Backend API Document for Dowadream", 
        terms_of_service="https://www.google.com/policies/terms/", 
        contact=openapi.Contact(name="admin", email=settings.MAIL_ADDRESS), 
        license=openapi.License(name="BSD License"), 
    ), 
    public=True, 
    permission_classes=(permissions.AllowAny,), 
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('search/', include('search.urls')),
  
    path('user/', include('user.urls')),
    path('user/', include('dj_rest_auth.urls')),
    path('user/', include('allauth.urls')),
    
    path('review/', include('review.urls')),
    path('program/', include('program.urls'))
]

# DEBUG 모드 켜져있을때만 swagger 문서가 보이도록 해주는 설정
if settings.DEBUG:
    urlpatterns += [
        re_path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
