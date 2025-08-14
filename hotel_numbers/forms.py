from django.core.exceptions import ValidationError
from django.utils import timezone
from django import forms

from hotel_numbers.models import Hotel, Room, Booking


class BookingSiteForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'guest_name']

    def clean_start_date(self):
        date = self.cleaned_data.get('start_date')
        if date and date < timezone.now().date():
            raise ValidationError("Нельзя забронировать номер в прошлом")
        return date

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date:
            if end_date <= start_date:
                raise ValidationError('Дата выезда должна быть позже даты заезда')
        room = cleaned_data.get('room')
        if room and start_date and end_date:
            overlapping = Booking.objects.filter(room=room, start_date__lt=end_date,
                                                 end_date__gt=start_date).exists()
            if overlapping:
                raise ValidationError('На эти даты номер уже забронирован')
        return cleaned_data


class BookingApiForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'start_date', 'end_date', 'guest_name']

    def clean_start_date(self):
        date = self.cleaned_data.get('start_date')
        if date and date < timezone.now().date():
            raise ValidationError("Нельзя забронировать номер в прошлом")
        return date

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date:
            if end_date <= start_date:
                raise ValidationError('Дата выезда должна быть позже даты заезда')
        room = cleaned_data.get('room')
        if room and start_date and end_date:
            overlapping = Booking.objects.filter(room=room, start_date__lt=end_date,
                                                 end_date__gt=start_date).exists()
            if overlapping:
                raise ValidationError('На эти даты номер уже забронирован')
        return cleaned_data


class RoomForm(forms.ModelForm):
    hotel = forms.ModelChoiceField(
        queryset=Hotel.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = Room
        fields = ['title', 'price', 'sleep_places', 'floor', 'category', 'hotel']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Цена за ночь должна быть больше нуля')
        return price

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        hotel = cleaned_data.get('hotel')
        if title and hotel:
            if Room.objects.filter(hotel=hotel, title=title).exists():
                raise ValidationError(f'Номер с названием {title} в отеле '
                                      f'{hotel.title} уже присутствует')
        return cleaned_data
