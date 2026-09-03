from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'guest_name', 'check_in', 'check_out', 'status', 'is_paid')
    list_filter = ('status', 'is_paid', 'room')
    search_fields = ('guest_name', 'guest_phone', 'guest_email')
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    actions = ['confirm_bookings', 'cancel_bookings']

    def confirm_bookings(self, request, queryset):
        queryset.update(status='confirmed')
    confirm_bookings.short_description = "Подтвердить выбранные"

    def cancel_bookings(self, request, queryset):
        queryset.update(status='canceled')
    cancel_bookings.short_description = "Отменить выбранные"