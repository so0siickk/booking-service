from django.utils import timezone
from django.http import HttpResponseNotFound
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from hotel_numbers.forms import BookingSiteForm
from hotel_numbers.models import Hotel, Room, Booking


def main(request):
    hotels = Hotel.objects.all()
    data = {
        'hotels': hotels
    }
    return render(request, 'hotel_numbers/main.html', context=data)


def hotel_list(request):
    hotels = Hotel.objects.all()
    data = {
        'hotels': hotels
    }
    return render(request, 'hotel_numbers/hotel_list.html', context=data)


def hotel_detail(request, hotel_slug):
    hotel = Hotel.objects.get(slug=hotel_slug)
    unique_rooms_by_category = Room.objects.filter(hotel=hotel).order_by('category', '-price').distinct('category')
    data = {
        'hotel': hotel,
        'rooms_by_category': unique_rooms_by_category
    }
    return render(request, 'hotel_numbers/hotel_detail.html', context=data)


def room_list(request, hotel_slug, category):
    sort_option = request.GET.get('sort', 'price_asc')
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    rooms_query = Room.objects.filter(hotel=hotel, category=category)
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
    category_choices = dict(Room.Categories.choices)
    category_name = category_choices.get(category, category)
    data = {
        'rooms': rooms,
        'hotel': hotel,
        'category_name': category_name,
        'current_sort': sort_option
    }
    return render(request, 'hotel_numbers/room_list.html', context=data)


def room_preview(request, hotel_slug, room_slug):
    room = get_object_or_404(Room, slug=room_slug, hotel__slug=hotel_slug)
    form = None
    if request.method == "POST":
        form = BookingSiteForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            overlapping_bookings = Booking.objects.filter(
                room=room,
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exists()

            if overlapping_bookings:
                form.add_error(None, f'Номер забронирован на эти даты')
            else:
                booking = form.save(commit=False)
                booking.room = room
                booking.save()
                messages.success(request,
                                 f"Отлично! Номер '{room.title}' забронирован с"
                                 f" {booking.start_date.strftime('%d.%m.%Y')} по"
                                 f" {booking.end_date.strftime('%d.%m.%Y')}.")
                return redirect('hotel_numbers:room_preview', hotel_slug=hotel_slug, room_slug=room_slug)
    if form is None:
        form = BookingSiteForm()
    today = timezone.now().date()
    current_booking = room.bookings.filter(start_date__lte=today, end_date__gte=today).first()
    future_bookings = room.bookings.filter(start_date__gte=today).order_by('start_date')
    data = {
        'room': room,
        'form': form,
        'current_booking': current_booking,
        'future_bookings': future_bookings
    }
    return render(request, 'hotel_numbers/room_preview.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound(f"<h1>Такой страницы нет</h1>")
