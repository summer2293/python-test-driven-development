# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Item

def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
    #return render(request, 'home.html')
    # return HttpResponse('<html><title>To-do lists</title></html>')


