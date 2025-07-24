from django.utils import timezone
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from hotel_numbers.forms import BookingForm
from hotel_numbers.models import Hotels, Rooms, Booking


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


def hotel_detail(request, hotel_slug):
    hotel = Hotels.objects.get(slug=hotel_slug)
    # unique_rooms_by_category = Rooms.objects.filter(pk__in=rooms_id) для postgres
    unique_rooms_by_category = []
    category_seen = []
    all_rooms = Rooms.objects.all()
    for room in all_rooms:
        if room.category not in category_seen:
            unique_rooms_by_category.append(room)
            category_seen.append(room.category)
    data = {
        'hotel': hotel,
        'rooms_by_category': unique_rooms_by_category
    }
    return render(request, 'hotel_numbers/hotel_detail.html', context=data)


def room_list(request, hotel_slug, category):
    sort_option = request.GET.get('sort', 'price_asc')
    hotel = get_object_or_404(Hotels, slug=hotel_slug)
    rooms_query = Rooms.objects.filter(hotel=hotel, category=category)
    match sort_option:
        case 'price_asc':
            rooms = rooms_query.order_by('price')
        case 'price_desc':
            rooms = rooms_query.order_by('-price')
        case 'date_asc':
            rooms = rooms_query.order_by('date_added')
        case 'date_desc':
            rooms = rooms_query.order_by('-date_added')
        case _:
            rooms = rooms_query.order_by('price')
    category_choices = dict(Rooms.Categories.choices)
    category_name = category_choices.get(category, category)
    data = {
        'rooms': rooms,
        'hotel': hotel,
        'category_name': category_name,
        'current_sort': sort_option
    }
    return render(request, 'hotel_numbers/room_list.html', context=data)


def room_preview(request, hotel_slug, room_slug):
    room = get_object_or_404(Rooms, slug=room_slug,hotel__slug=hotel_slug)
    form = None
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            overlapping_bookings = Booking.objects.filter(
                room=room,
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exists()

            if overlapping_bookings:
                form.add_error(None,f'Номер забронирован на эти даты')
            else:
                Booking.objects.create(start_date=form.cleaned_data.get('start_date'),
                                       end_date=form.cleaned_data.get('end_date'),
                                       room=room,
                                       )
                return redirect('hotel_numbers:room_preview', hotel_slug=hotel_slug, room_slug=room_slug)
    if form is None:
        form = BookingForm()
    today = timezone.now()
    current_booking = room.bookings.filter(start_date__lte=today, end_date__gte=today).first()
    data = {
        'room': room,
        'form': form,
        'current_booking': current_booking
    }
    return render(request, 'hotel_numbers/room_preview.html', context=data)


def add_hotel(request, hotel_id):
    return render(request, 'hotel_numbers/hotel_add')


def add_room(request, hotel_id, category, room_id):
    return render(request, 'hotel_numbers/room_add')


def page_not_found(request, exception):
    return HttpResponseNotFound(f"<h1>Такой страницы нет</h1>")
