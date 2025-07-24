from django.core.exceptions import ValidationError
from django.utils import timezone
from django import forms


class BookingForm(forms.Form):
    start_date = forms.DateField(label='Дата заезда',
                                 widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='Дата выезда',
                               widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_start_date(self):
        date = self.cleaned_data.get('start_date')
        if date and date < timezone.now().date():
            raise ValidationError("Нельзя забронировать номер в прошлом")
        return date

    def clean(self):
        cleaned_date = super().clean()
        start_date = cleaned_date.get('start_date')
        end_date = cleaned_date.get('end_date')

        if start_date and end_date:
            if end_date <= start_date:
                raise ValidationError("Дата выезда должна быть позже даты заезда")
        return cleaned_date
