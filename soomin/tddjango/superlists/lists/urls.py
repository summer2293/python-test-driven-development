from django.conf.urls import patterns, include, url
from django.contrib import admin
urlpatterns = [ 
    url(r'Aadmin/', include(admin.site.urls)),
]