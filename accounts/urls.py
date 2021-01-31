from django.urls import path, include
from .api import RequestPasswordResetAPI, LoginAPI, RegisterAPI
from knox import views as knox_views
urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/forgot', RequestPasswordResetAPI.as_view())
]
