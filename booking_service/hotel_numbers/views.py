from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.urls import reverse
from django.shortcuts import render, redirect

from hotel_numbers.models import Hotels, Rooms


# Create your views here.

def main(request):
    hotels = Hotels.objects.all()
    data = {
        'hotels': hotels
    }
    return render(request, 'hotel_numbers/main.html', context=data)


def hotel_list(request):
    hotels = Hotels.objects.all()
    data = {
        'hotels': hotels
    }
    return render(request, 'hotel_numbers/hotel_list.html', context=data)


def categories(request, hotel_id):
    return render(request, 'hotel_numbers/categories')


def room_list(request, hotel_id, category):
    rooms = Rooms.objects.all()
    data = {
        'room': rooms
    }
    return render(request, 'hotel_numbers/room_list',context=data)


def room_preview(request, hotel_id, category, room_id):
    return render(request, 'hotel_numbers/room_detail')


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