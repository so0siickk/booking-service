from django.urls import path
from . import views

app_name = 'hotel_numbers'

urlpatterns = [
    path('', views.main, name='home'),
    path('hotels/',views.hotel_list, name='hotel_list'),
    path('hotels/<slug:hotel_slug>/', views.hotel_detail, name='hotel_detail'),
    path('hotels/<slug:hotel_slug>/<str:category>/', views.room_list, name='room_list'),
    path('hotels/<slug:hotel_slug>/room/<slug:room_slug>/', views.room_preview, name='room_preview'),
]