from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('lists/the-only-list-in-the-world/', views.view_list),
]