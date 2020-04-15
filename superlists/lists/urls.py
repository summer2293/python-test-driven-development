# from django.conf.urls import include
from django.urls import path
from . import views  # 이런식으로 import 하면 붉은 밑줄도  안 나타나고 좋네요

urlpatterns = [
    path('', views.home_page),
]