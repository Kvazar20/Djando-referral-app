from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('enter-phone/', views.enter_phone, name='enter-phone'),
    path('enter-code/', views.enter_code, name='enter-code'),
    path('profile/', views.profile, name='profile'),
    path('api/token/', obtain_auth_token, name='obtain_token'),
]