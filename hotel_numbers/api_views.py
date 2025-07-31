import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from hotel_numbers.models import Room, Booking
from hotel_numbers.forms import BookingApiForm, RoomForm
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def room_list_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        form = RoomForm(data)
        if form.is_valid():
            new_room = form.save()
            return JsonResponse({'room_id': new_room.id}, status=201,
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'errors': form.errors}, status=400,
                                json_dumps_params={'ensure_ascii': False})
    elif request.method == 'GET':
        hotel_id = request.GET.get('hotel_id')
        if not hotel_id:
            return JsonResponse({'error': 'Hotel_id parameter is required'}, status=400)
        sort_by = request.GET.get('sort', 'date_added')
        if sort_by not in ('date_added', '-date_added', 'price', '-price'):
            sort_by = 'date_added'
        rooms = Room.objects.filter(hotel_id=hotel_id).order_by(sort_by)
        data_to_return = list(rooms.values('id', 'title', 'price', 'slug'))
        return JsonResponse(data_to_return, safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@require_http_methods(["GET", "DELETE"])
def room_detail_delete(request, room_id):
    try:
        room = Room.objects.get(pk=room_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)
    if request.method == 'DELETE':
        room.bookings.all().delete()
        room.delete()
        return HttpResponse(status=204)
    elif request.method == 'GET':
        data_to_return = {
            'id': room.id,
            'title': room.title,
            'price': str(room.price),
            'sleep_places': room.sleep_places,
            'floor': room.floor,
            'category': room.get_category_display(),
            'hotel_id': room.hotel_id
        }
        return JsonResponse(data_to_return, status=200, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def booking_list_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        form = BookingApiForm(data)
        if form.is_valid():
            new_booking = form.save()
            return JsonResponse({'booking_id': new_booking.id}, status=201,
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'errors': form.errors}, status=400,
                                json_dumps_params={'ensure_ascii': False})
    elif request.method == 'GET':
        room_id = request.GET.get('room_id')
        if not room_id:
            return JsonResponse({'error': 'Room_id parameter is required'}, status=400)
        sort = 'start_date'
        bookings = Booking.objects.filter(room_id=room_id).order_by(sort)
        data_to_return = list(bookings.values('id', 'start_date', 'end_date'))
        return JsonResponse(data_to_return, safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@require_http_methods(["DELETE"])
def booking_delete(request, booking_id):
    try:
        booking = Booking.objects.get(pk=booking_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Booking not found'}, status=404,
                            json_dumps_params={'ensure_ascii': False})
    booking.delete()
    return HttpResponse(status=204)
