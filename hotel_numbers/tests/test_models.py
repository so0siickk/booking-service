import pytest
from hotel_numbers.models import Room, Hotel
from django.utils.text import slugify
from transliterate import translit


@pytest.mark.django_db
def test_room_slug_creation_on_save():
    test_hotel = Hotel.objects.create(title='Тестовый отель', city='Краснодар')
    room_title = 'Тестовая комната'
    test_room = Room.objects.create(
        title=room_title,
        price=5000,
        sleep_places=2,
        floor=9,
        hotel_id=test_hotel.id,
        category='RG'
    )
    test_room.save()
    assert test_room.slug == slugify(translit(room_title, 'ru', reversed=True))


@pytest.mark.django_db
def test_hotel_slug_creation_on_save():
    hotel_title = 'Тестовый отель'
    test_hotel = Hotel.objects.create(title=hotel_title, city='Краснодар')
    test_hotel.save()
    assert test_hotel.slug == slugify(translit(hotel_title, 'ru', reversed=True))
