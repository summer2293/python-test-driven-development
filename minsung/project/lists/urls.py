from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('lists/<int:list_id>/', views.view_list, name='view_list'),
    path('lists/new', views.new_list, name='new_list'),
]