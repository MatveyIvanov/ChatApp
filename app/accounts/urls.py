from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import auth, logout


urlpatterns = [
    path('auth', auth, name='auth'),
    path('logout', logout, name='logout'),
]