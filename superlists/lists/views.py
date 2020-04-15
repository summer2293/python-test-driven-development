from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    # pass
    return HttpResponse('<html><title>To-do lists</title></html>')