from django.contrib import admin
from django.urls import path, include

from tracker import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(
    'api/logs',
    views.StudyLogViewSet,
    basename='logs'
)


urlpatterns = [

    # Website URLs
    path('', include('tracker.urls')),

    # Admin
    path('admin/', admin.site.urls),

    
    # JWT
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    
    # Router URLs
    path('', include(router.urls)),

]