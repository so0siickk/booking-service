from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.shortcuts import render, redirect


# Create your views here.

def index(request):
    return HttpResponse("Сайт с бронированием")


def hotels(request):
    return HttpResponse("Отели")


def categories(request, hotel_id):
    return HttpResponse(f"<h1>Категории номеров</h1><p>Типы комнат<p>")


def room_variants(request, hotel_id, category):
    return HttpResponse("Варианты комнат")


def room_preview(request, hotel_id, category, room_id):
    return HttpResponse(f"Комната{room_id}")


def plans_for_future(request, year):
    if year > 2025:
        print(year)
        #uri = reverse('categories', args=(1,))
        return redirect('home',)
    else:
        return HttpResponse(f"Планы отеля на год{year}:")


def page_not_found(request, exception):
    return HttpResponseNotFound(f"<h1>Такой страницы нет</h1>")

#http://youtube.com/watch?v=cFPWBKORMlg&list=PLA0M1Bcd0w8yU5h2vwZ4LO7h1xt8COUXl