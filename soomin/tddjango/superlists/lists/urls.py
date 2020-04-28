from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [
    url("", views.home_page, name="home"),
    url(r"^lists/the-only-list-in-the-world/$", views.view_list, name="view_list"),
]
