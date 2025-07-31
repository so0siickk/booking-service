from datetime import date, timedelta

import pytest
import json
from hotel_numbers.models import *


@pytest.fixture
def test_hotel(db):
    return Hotel.objects.create(title='Тестовый отель', city='Краснодар')


@pytest.fixture
def test_rooms(test_hotel):
    test_rooms = []
    for i in range(1, 4):
        test_rooms.append(Room.objects.create(
            title=f'Тестовый номер {i}',
            price=5000 + i,
            sleep_places=2,
            floor=9,
            hotel_id=test_hotel.id,
            category='RG'
        ))
    return test_rooms


@pytest.fixture
def test_booking(test_rooms):
    test_booking = Booking.objects.create(
        start_date=date.today(),
        end_date=date.today() + timedelta(days=2),
        guest_name='Тестовый гость',
        room_id=test_rooms[0].id
    )
    return test_booking


@pytest.mark.django_db
def test_room_list_success_get(client, test_hotel, test_rooms):
    url = f"/api/rooms/?hotel_id={test_hotel.id}"
    response = client.get(url)
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 3
    assert response_data[0]['title'] == 'Тестовый номер 1'
    assert response_data[1]['price'] == '5002.00'


@pytest.mark.django_db
def test_room_list_fail_get(client):
    url = f"/api/rooms/?hotel_id="
    response = client.get(url)
    assert response.status_code == 400
    response_data = response.json()
    assert response_data['error'] == 'Hotel_id parameter is required'


@pytest.mark.django_db
def test_room_list_success_create(client, test_hotel):
    url = f"/api/rooms/"
    test_data = {
        'title': 'Комната для данного теста',
        'price': '5050',
        'sleep_places': 4,
        'floor': 5,
        'category': 'UP',
        'hotel': test_hotel.id,
    }
    response = client.post(url, data=json.dumps(test_data), content_type='application/json')
    assert response.status_code == 201
    response_data = response.json()
    assert 'room_id' in response_data
    test_room = Room.objects.get(pk=response_data['room_id'])
    assert test_room.title == 'Комната для данного теста'
    assert test_room.sleep_places == 4


@pytest.mark.django_db
def test_room_list_fail_create(client, test_hotel):
    url = f"/api/rooms/"
    test_data = {
        'title': 'Комната для данного теста',
        'price': '5050',
        'sleep_places': 4,
        'floor': 5,
        'hotel': test_hotel.id,
    }
    response = client.post(url, data=json.dumps(test_data), content_type='application/json')
    assert response.status_code == 400
    response_data = response.json()
    assert 'errors' in response_data


@pytest.mark.django_db
def test_room_detail_success_get(client, test_rooms):
    test_room = test_rooms[0]
    url = f"/api/rooms/{test_room.id}/"
    response = client.get(url)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['floor'] == 9
    assert response_data['category'] == 'Обычный'


@pytest.mark.django_db
def test_room_detail_fail_get(client):
    url = f"/api/rooms/1/"
    response = client.get(url)
    assert response.status_code == 404
    response_data = response.json()
    assert response_data['error'] == 'Room not found'


@pytest.mark.django_db
def test_room_success_delete(client, test_hotel, test_rooms):
    test_room = test_rooms[-1]
    url = f"/api/rooms/{test_room.id}/"
    response = client.delete(url)
    assert response.status_code == 204
    url = f"/api/rooms/?hotel_id={test_hotel.id}"
    response = client.get(url)
    response_data = response.json()
    assert len(response_data) == len(test_rooms) - 1


@pytest.mark.django_db
def test_room_fail_delete(client):
    url = f"/api/rooms/1/"
    response = client.delete(url)
    assert response.status_code == 404
    response_data = response.json()
    assert response_data['error'] == 'Room not found'


@pytest.mark.django_db
def test_booking_list_success_create(client, test_rooms):
    test_room = test_rooms[-1]
    url = '/api/bookings/'
    test_data = {
        'start_date': (date.today()).isoformat(),
        'end_date': (date.today() + timedelta(days=5)).isoformat(),
        'guest_name': 'Гость для данного теста',
        'room': test_room.id
    }
    response = client.post(url, data=json.dumps(test_data), content_type='application/json')
    assert response.status_code == 201
    response_data = response.json()
    assert 'booking_id' in response_data
    current_test_booking = Booking.objects.get(pk=response_data['booking_id'])
    assert current_test_booking.guest_name == 'Гость для данного теста'
    assert current_test_booking.room.id == test_room.id


@pytest.mark.django_db
def test_booking_list_fail_create(client, test_rooms):
    test_room = test_rooms[-1]
    url = '/api/bookings/'
    test_data = {
        'start_date': (date.today()).isoformat(),
        'end_date': (date.today() - timedelta(days=5)).isoformat(),
        'guest_name': 'Гость для данного теста',
        'room': test_room.id
    }
    response = client.post(url, data=json.dumps(test_data), content_type='application/json')
    assert response.status_code == 400
    response_data = response.json()
    assert 'errors' in response_data


@pytest.mark.django_db
def test_booking_list_success_get(client, test_rooms, test_booking):
    test_room = test_rooms[0]
    url = f'/api/bookings/?room_id={test_room.id}'
    response = client.get(url)
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    assert response_data[0]['start_date'] == date.today().isoformat()


@pytest.mark.django_db
def test_booking_list_fail_get(client):
    url = f'/api/bookings/?room_id='
    response = client.get(url)
    assert response.status_code == 400
    response_data = response.json()
    assert response_data['error'] == 'Room_id parameter is required'


@pytest.mark.django_db
def test_booking_success_delete(client, test_booking):
    url = f'/api/bookings/{test_booking.id}/'
    response = client.delete(url)
    assert response.status_code == 204
    assert not Booking.objects.filter(pk=test_booking.id).exists()


@pytest.mark.django_db
def test_booking_fail_delete(client):
    url = f'/api/bookings/1000000/'
    response = client.delete(url)
    assert response.status_code == 404
    response_data = response.json()
    assert response_data['error'] == 'Booking not found'
