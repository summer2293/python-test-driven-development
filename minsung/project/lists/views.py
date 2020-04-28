from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Item


def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'lists/home.html')


def view_list(request):
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, 'lists/list.html', context)