from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/mypost/', mypost, name='mypost'),
]