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

class RoomDetailView(DetailView):
    model = Room
    template_name = 'rooms/room_detail.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.get_object()
        # Получаем занятые даты для календаря
        bookings = Booking.objects.filter(
            room=room,
            status__in=['pending', 'confirmed']
        ).values_list('check_in', 'check_out')
        events = []
        for check_in, check_out in bookings:
            events.append({
                'start': check_in.isoformat(),
                'end': check_out.isoformat(),
                'display': 'background',
                'color': '#D4884A',
            })
        context['booked_events'] = json.dumps(events)
        return context