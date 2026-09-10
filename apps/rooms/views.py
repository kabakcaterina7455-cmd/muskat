from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Room
from apps.bookings.models import Booking
import json

class RoomListView(ListView):
    model = Room
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'
    queryset = Room.objects.filter(is_active=True)

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from datetime import date, timedelta
import json
from .models import Room
from apps.bookings.models import Booking


class RoomListView(ListView):
    model = Room
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'
    queryset = Room.objects.filter(is_active=True)


class RoomDetailView(DetailView):
    model = Room
    template_name = 'rooms/room_detail.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.get_object()

        # Считаем занятость по дням на 3 месяца вперёд
        today = date.today()
        end_date = today + timedelta(days=90)

        bookings = Booking.objects.filter(
            room=room,
            status__in=['pending', 'confirmed'],
            check_in__lte=end_date,
            check_out__gte=today
        ).values_list('check_in', 'check_out')

        # Заполняем словарь: {дата: количество занятых номеров}
        occupied = {}
        for check_in, check_out in bookings:
            current = max(check_in, today)
            while current < check_out:
                key = current.isoformat()
                occupied[key] = occupied.get(key, 0) + 1
                current += timedelta(days=1)

        # Передаём в шаблон: количество всего номеров и словарь занятости
        context['room_quantity'] = room.quantity
        context['occupied_by_day'] = json.dumps(occupied)
        return context