from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists import models

# Create your views here.
def home_page(request):
    if request.method == "POST":
        return render(request, 'home.html')

    items = models.Item.objects.all()
    return render(request, 'home.html')

def view_list(request, list_id):
    list_ = models.List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})

def new_list(request):
    list_ = models.List.objects.create()
    item = models.Item.objects.create(text=request.POST['item_text'],
                                      list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect(f'/lists/{list_.id}/')

def add_item(request, list_id):
    list_ = models.List.objects.get(id=list_id)
    item = models.Item.objects.create(text=request.POST['item_text'],
                                      list=list_)
    try:
        item.full_clean()
    except ValidationError:
        return render(request, 'home.html')
    return redirect(f'/lists/{list_.id}/') 
