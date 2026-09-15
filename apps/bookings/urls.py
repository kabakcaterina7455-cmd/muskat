
from django.urls import path
from .views import BookingCreateView, BookingSuccessView, BookingCancelView, calculate_price

app_name = 'bookings'

urlpatterns = [
    path('create/<slug:room_slug>/', BookingCreateView.as_view(), name='create'),
    path('success/<int:booking_id>/', BookingSuccessView.as_view(), name='success'),
    path('cancel/<int:booking_id>/', BookingCancelView.as_view(), name='cancel'),
    path('calculate/<slug:room_slug>/', calculate_price, name='calculate'),
]