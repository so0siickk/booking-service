from datetime import date, timedelta
import pytest
from hotel_numbers.forms import BookingApiForm, RoomForm
from hotel_numbers.models import Hotel, Room


@pytest.mark.django_db
def test_booking_form_from_success_on_valid_data():
    test_hotel = Hotel.objects.create(title='Тестовый отель', city='Краснодар')
    test_room = Room.objects.create(
        title='Тестовая комната',
        price=5000,
        sleep_places=2,
        floor=9,
        hotel_id=test_hotel.id,
        category='RG'
    )
    start_date = date.today()
    end_date = date.today() + timedelta(days=1)
    form_data = {
        'room': test_room,
        'start_date': start_date,
        'end_date': end_date,
        'guest': 'Тестовый гость'
    }
    form = BookingApiForm(data=form_data)
    assert form.is_valid()
    assert form.cleaned_data['start_date'] == start_date
    assert form.cleaned_data['end_date'] == end_date


def test_booking_form_from_fail_on_past_date():
    yesterday = date.today() - timedelta(days=1)
    tomorrow = date.today() + timedelta(days=1)
    form_data = {
        'start_date': yesterday,
        'end_date': tomorrow
    }
    form = BookingApiForm(data=form_data)
    assert not form.is_valid()
    assert 'start_date' in form.errors
    assert "Нельзя забронировать номер в прошлом" in form.errors['start_date'][0]


@pytest.mark.django_db
def test_room_form_from_fail_on_valid_data():
    test_hotel = Hotel.objects.create(title='Тестовый отель', city='Краснодар')
    title = 'Тестовый номер'
    price = -5000.50
    sleep_places = 3
    floor = 5
    category = 'DX'
    hotel = test_hotel.id
    form_data = {
        'title': title,
        'price': price,
        'sleep_places': sleep_places,
        'floor': floor,
        'category': category,
        'hotel': hotel
    }
    form = RoomForm(data=form_data)
    is_valid = form.is_valid()
    assert not is_valid
    assert 'price' in form.errors
    assert 'Цена за ночь должна быть больше нуля' in form.errors['price'][0]


@pytest.mark.django_db
def test_room_form_from_success_on_valid_data():
    test_hotel = Hotel.objects.create(title='Тестовый отель', city='Краснодар')
    title = 'Тестовый номер'
    price = 5000.50
    sleep_places = 3
    floor = 5
    category = 'DX'
    hotel = test_hotel.id
    form_data = {
        'title': title,
        'price': price,
        'sleep_places': sleep_places,
        'floor': floor,
        'category': category,
        'hotel': hotel
    }
    form = RoomForm(data=form_data)
    is_valid = form.is_valid()
    if not is_valid:
        print(form.errors)
    assert is_valid, "Форма должна быть валидной с корректными данными"
    assert form.cleaned_data['category'] == 'DX'
    assert form.cleaned_data['hotel'] == test_hotel
    assert form.cleaned_data['title'] == 'Тестовый номер'
