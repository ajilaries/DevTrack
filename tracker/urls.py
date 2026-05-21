from django.urls import path
from . import views

urlpatterns = [

    # Website Routes
    path('', views.landing, name='landing'),

    path('signup/', views.signup_view, name='signup'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('home/', views.home, name='home'),

    path('profile/', views.profile_view, name='profile'),

    
    # Study Logs
    path('add/', views.add_log, name='add_log'),

    path(
        'edit/<int:id>/',
        views.edit_log,
        name='edit_log'
    ),

    path(
        'delete/<int:id>/',
        views.delete_log,
        name='delete_log'
    ),

    
    # API Routes
    path(
        'api/logs/',
        views.api_logs,
        name='api_logs'
    ),

    path(
        'api/logs/<int:id>/',
        views.SingleStudyLogAPIView.as_view(),
        name='single_log_api'
    ),
    # Notifications Routes
    path(
        'notifications/',
        views.notifications_page,
        name='notifications'
    ),

    path(
        'notifications/read/<int:id>/',
        views.mark_notification_read,
        name='mark_notification_read'
    ),
]