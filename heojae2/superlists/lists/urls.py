from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('lists/<int:list_id>/', views.view_list),
    path('lists/<int:list_id>/add_item', views.add_item),
    path('lists/new', views.new_list),
]