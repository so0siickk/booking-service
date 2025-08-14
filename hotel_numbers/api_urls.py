from django.urls import path
from . import api_views

app_name = 'api'

urlpatterns = [
    path('rooms/', api_views.room_list_create, name='room_list_create'),
    path('rooms/<int:room_id>/', api_views.room_detail_delete, name='room_detail_delete'),
    path('bookings/', api_views.booking_list_create, name='booking_list_create'),
    path('bookings/<int:booking_id>/', api_views.booking_delete, name='booking_delete'),
]
