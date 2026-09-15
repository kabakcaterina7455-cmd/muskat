from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Админка бронирований."""

    list_display = (
        'id', 'room', 'guest_name', 'check_in', 'check_out',
        'created_at', 'status', 'is_paid'
    )
    list_filter = ('status', 'is_paid', 'room', 'created_at')
    search_fields = ('guest_name', 'guest_phone', 'guest_email')
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    actions = ['confirm_bookings', 'cancel_bookings', 'send_confirmation_email']

    def confirm_bookings(self, request, queryset):
        """Подтвердить выбранные брони и отправить письма."""
        count = 0
        for booking in queryset:
            booking.status = 'confirmed'
            booking.save()  # ← вызовет сигнал pre_save и отправит письмо
            count += 1
        self.message_user(request, f"Подтверждено броней: {count}. Письма отправлены.")
    confirm_bookings.short_description = "✅ Подтвердить выбранные"

    def cancel_bookings(self, request, queryset):
        """Отменить выбранные брони и отправить письма."""
        count = 0
        for booking in queryset:
            booking.status = 'canceled'
            booking.save()  # ← вызовет сигнал pre_save и отправит письмо
            count += 1
        self.message_user(request, f"Отменено броней: {count}. Письма отправлены.")
    cancel_bookings.short_description = "❌ Отменить выбранные"

    def send_confirmation_email(self, request, queryset):
        """Вручную отправить письмо-подтверждение (без смены статуса)."""
        sent = 0
        for booking in queryset:
            send_mail(
                subject=f"Бронь #{booking.id} подтверждена!",
                message=(
                    f"Здравствуйте, {booking.guest_name}!\n\n"
                    f"Ваша бронь на номер «{booking.room.name}» "
                    f"с {booking.check_in} по {booking.check_out} подтверждена.\n\n"
                    f"Стоимость: {booking.total_price} ₽\n\n"
                    f"Ждём вас!\n\n"
                    f"С уважением,\nГостевой дом «Мускат»"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.guest_email],
                fail_silently=True,
            )
            sent += 1
        self.message_user(request, f"Отправлено писем: {sent}")
    send_confirmation_email.short_description = "📧 Отправить письмо-подтверждение"