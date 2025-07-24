from django.db import models
from django.db.models import PROTECT
from django.urls import reverse


class BookedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Rooms.Status.BOOKED)


class AvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Rooms.Status.AVAILABLE)


class Hotels(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название отеля')
    city = models.CharField(max_length=255, verbose_name='Город', db_index=True)
    slug = models.SlugField(max_length=255, db_index=True)

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'


class Rooms(models.Model):
    class Status(models.IntegerChoices):
        BOOKED = 0, 'Зарезервирован'
        AVAILABLE = 1, 'Свободен'

    class Categories(models.TextChoices):
        REGULAR = 'RG', 'Обычный'
        UPDATED = 'UP', 'Улучшенный'
        DELUXE = 'DX', 'Делюкс'
        REPRESENTATIVE = 'RP', 'Представительский'

    title = models.CharField(max_length=255, verbose_name='Название номера')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True,
                                verbose_name='Цена за ночь')
    sleep_places = models.PositiveSmallIntegerField(verbose_name='Количество спальных мест')
    floor = models.PositiveSmallIntegerField(default=1, verbose_name='Этаж')
    category = models.CharField(max_length=2, choices=Categories.choices,
                                default=Categories.REGULAR, verbose_name='Категория')
    status = models.IntegerField(default=Status.AVAILABLE, choices=Status.choices,
                                 db_index=True, verbose_name='Статус')
    slug = models.SlugField(max_length=255, db_index=True, verbose_name='Ссылка')
    hotel: Hotels = models.ForeignKey('Hotels', on_delete=PROTECT,
                                      related_name='rooms', verbose_name='Отель')
    date_added = models.DateField(auto_now_add=True, verbose_name='Дата добавления', null=True)

    objects = models.Manager()
    booked = BookedManager()
    available = AvailableManager()

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def __str__(self):
        return f'{self.title} в отеле {self.hotel.title}, категория:{self.category}'

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'
        ordering = ['hotel', 'price']


class Booking(models.Model):
    start_date = models.DateField(verbose_name='Дата начала бронирования')
    end_date = models.DateField(verbose_name='Дата окончания бронирования')
    room: 'Rooms' = models.ForeignKey('Rooms', on_delete=PROTECT,
                                      related_name='bookings', verbose_name='Номер комнаты')
    guest_name = models.CharField(max_length=255, verbose_name='Имя гостя', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания брони')

    objects = models.Manager()

    def __str__(self):
        return f'Бронь номера {self.room.title} в отеле {self.start_date} по {self.end_date}'

    class Meta:
        verbose_name = 'Бронирования'
        verbose_name_plural = 'Бронирования'
        ordering = ['created_at']
