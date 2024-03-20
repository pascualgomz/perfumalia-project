from django.urls import path
from .views import *


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', index, name='index'),
]