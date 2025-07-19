from django.db import models
from django.db.models import PROTECT


class BookedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Rooms.Status.BOOKED)


class AvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Rooms.Status.AVAILABLE)


class Hotels(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название отеля')
    city = models.CharField(max_length=255, verbose_name='Город', db_index=True)

    objects = models.Manager()


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
    date_start_booked = models.DateField(null=True, blank=True,
                                         verbose_name='Дата начала бронирования')
    date_end_booked = models.DateField(null=True, blank=True,
                                       verbose_name='Дата конца бронирования')
    hotel: Hotels = models.ForeignKey('Hotels', on_delete=PROTECT,
                                      related_name='rooms', verbose_name='Отель')

    objects = models.Manager()
    booked = BookedManager()
    available = AvailableManager()

    def __str__(self):
        return f'{self.title} в отеле {self.hotel.title}'

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'
        ordering = ['hotel', 'price']
