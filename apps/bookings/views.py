from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
from django.urls import reverse
from .models import Booking
from apps.rooms.models import Room
from .forms import BookingForm

class BookingCreateView(View):
    def get(self, request, room_slug):
        room = get_object_or_404(Room, slug=room_slug, is_active=True)
        form = BookingForm(initial={'room': room})
        return render(request, 'bookings/booking_form.html', {'room': room, 'form': form})

    def post(self, request, room_slug):
        room = get_object_or_404(Room, slug=room_slug, is_active=True)
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            if not self.is_room_available(room, check_in, check_out):
                messages.error(request, "Выбранные даты заняты. Выберите другие.")
                return render(request, 'bookings/booking_form.html', {'room': room, 'form': form})

            booking = form.save(commit=False)
            booking.room = room
            if request.user.is_authenticated:
                booking.user = request.user
            booking.total_price = booking.calculate_total_price()
            booking.save()

            self.send_notifications(booking)

            messages.success(request, "Заявка отправлена! Мы свяжемся с вами.")
            return redirect(reverse('bookings:success', kwargs={'booking_id': booking.id}))
        return render(request, 'bookings/booking_form.html', {'room': room, 'form': form})

    def is_room_available(self, room, check_in, check_out):
        conflicting = Booking.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in,
            status__in=['pending', 'confirmed']
        )
        return not conflicting.exists()

    def send_notifications(self, booking):
        # Письмо гостю
        send_mail(
            subject=f"Заявка #{booking.id} принята",
            message=f"Здравствуйте, {booking.guest_name}!\n"
                    f"Ваша заявка на бронирование номера '{booking.room.name}' "
                    f"с {booking.check_in} по {booking.check_out} принята.\n"
                    f"Стоимость: {booking.total_price} руб.\nМы свяжемся с вами.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.guest_email],
            fail_silently=True,
        )
        # Письмо менеджеру
        send_mail(
            subject=f"Новая заявка #{booking.id}",
            message=f"Гость: {booking.guest_name}, тел. {booking.guest_phone}\n"
                    f"Номер: {booking.room.name}\nДаты: {booking.check_in}–{booking.check_out}\n"
                    f"Взрослых: {booking.adults}, детей: {booking.children}\nКомментарий: {booking.comment}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.MANAGER_EMAIL],
            fail_silently=True,
        )


class BookingSuccessView(View):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        return render(request, 'bookings/booking_success.html', {'booking': booking})