from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists import models
from lists.forms import EMPTY_LIST_ERROR, ItemForm


# Create your views here.
def home_page(request):
    if request.method == "POST":
        return render(request, 'home.html')

    items = models.Item.objects.all()
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    list_ = models.List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form':form})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = models.List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})

