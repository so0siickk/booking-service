from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")

app_name = 'hotel_numbers'

urlpatterns = [
    path('', views.main, name='home'),
    path('hotels/',views.hotel_list, name='hotel_list'),
    path('hotels/<int:hotel_id>/categories/', views.categories, name='categories'),
    path('hotels/<int:hotel_id>/<str:category>/', views.room_list, name='room_list'),
    path('hotels/<int:room_id>/', views.room_preview, name='room_preview'),
    path('plans/<year4:year>/', views.plans_for_future, name='future'),
]