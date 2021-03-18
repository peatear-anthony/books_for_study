from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists import models
from lists.forms import EMPTY_LIST_ERROR


# Create your views here.
def home_page(request):
    if request.method == "POST":
        return render(request, 'home.html')

    items = models.Item.objects.all()
    return render(request, 'home.html')

def view_list(request, list_id):
    list_ = models.List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item = models.Item.objects.create(text=request.POST['item_text'],
                                      list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            item.delete()
            error = EMPTY_LIST_ERROR
    return render(request, 'list.html', {'list': list_, 'error': error})

def new_list(request):
    list_ = models.List.objects.create()
    item = models.Item.objects.create(text=request.POST['item_text'],
                                      list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = EMPTY_LIST_ERROR
        return render(request, 'home.html', {"error": error})
    return redirect(list_)

