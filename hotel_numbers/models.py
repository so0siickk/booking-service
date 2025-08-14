from django.db import models
from django.db.models import PROTECT
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit


class Hotel(models.Model):
    title: str = models.CharField(max_length=255, verbose_name='Название отеля')
    city = models.CharField(max_length=255, db_index=True, verbose_name='Город')
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name='Ссылка')

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.title, 'ru', reversed=True))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'


class Room(models.Model):
    class Categories(models.TextChoices):
        REGULAR = 'RG', 'Обычный'
        UPDATED = 'UP', 'Улучшенный'
        DELUXE = 'DX', 'Делюкс'
        REPRESENTATIVE = 'RP', 'Представительский'

    title: str = models.CharField(max_length=255, verbose_name='Название номера')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True,
                                verbose_name='Цена за ночь')
    sleep_places = models.PositiveSmallIntegerField(verbose_name='Количество спальных мест')
    floor = models.PositiveSmallIntegerField(default=1, verbose_name='Этаж')
    category = models.CharField(max_length=2, choices=Categories.choices,
                                default=Categories.REGULAR, verbose_name='Категория')
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name='Ссылка')
    hotel: Hotel = models.ForeignKey('Hotel', on_delete=PROTECT,
                                     related_name='rooms', verbose_name='Отель')
    date_added = models.DateField(auto_now_add=True, verbose_name='Дата добавления', null=True)

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def __str__(self):
        return f'{self.title} в отеле {self.hotel.title}, категория:{self.category}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.title, 'ru', reversed=True))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'
        ordering = ['hotel', 'price']


class Booking(models.Model):
    start_date = models.DateField(verbose_name='Дата начала бронирования')
    end_date = models.DateField(verbose_name='Дата окончания бронирования')
    room: 'Room' = models.ForeignKey('Room', on_delete=PROTECT,
                                     related_name='bookings', verbose_name='Номер комнаты')
    guest_name = models.CharField(max_length=255, verbose_name='Имя гостя', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания брони')

    objects = models.Manager()

    def __str__(self):
        return f'Бронь номера {self.room.title} в отеле {self.start_date} по {self.end_date}'

    class Meta:
        verbose_name = 'Бронированиe'
        verbose_name_plural = 'Бронирования'
        ordering = ['created_at']

        constraints = [
            models.UniqueConstraint(
                fields=['room', 'start_date', 'end_date'],
                name='unique_booking_for_room_and_dates'
            )
        ]
