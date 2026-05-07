from django.urls import path
from . import views

urlpatterns = [

    path('',views.landing , name='landing'),
    path('signup/',views.signup_view, name='signpu'),
    path('login/',views.login_view,name='login'),
    path('/dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('add/',views.add_log, name='add_log'),
    path('delete/<int:id>/', views.delete_log, name='delete_log'),
    path('edit/<int:id>/',views.edit_log, name='edit_log')
]
