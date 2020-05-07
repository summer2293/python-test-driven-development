from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(f'/lists/{list_.id}/')
        except ValidationError:
            # error = "You can't have an empty list item"
            error = "빈 아이템을 등록할 수 없습니다"

    return render(request, 'list.html', {'list': list_, 'error': error})


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        # error = "아이템이 비어 있습니다"
        error = "빈 아이템을 등록할 수 없습니다"
        return render(request, 'home.html', {"error": error})
    return redirect(f'/lists/{list_.id}/')

