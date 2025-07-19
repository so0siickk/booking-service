from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),
    path('hotels/hotels/',views.hotels),
    path('hotels/<str:hotel_name>/categories/', views.categories),
    path('hotels/<str:hotel_name>/categories/<str:category>/room_variants', views.room_variants),
    path('hotels/<str:hotel_name>/categories/<str:category>/room_variants/<int:room_id>', views.room_preview),
    path('plans/<year4:year>/', views.plans_for_future),
]