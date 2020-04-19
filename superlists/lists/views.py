# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    # pass
    return render(request, 'home.html')
    # return HttpResponse('<html><title>To-do lists</title></html>')


