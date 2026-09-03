from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from apps.rooms.models import Room

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('canceled', 'Отменено'),
        ('completed', 'Завершено'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    guest_name = models.CharField(max_length=200, verbose_name="Имя гостя")
    guest_phone = models.CharField(max_length=20, verbose_name="Телефон")
    guest_email = models.EmailField(verbose_name="Email")
    check_in = models.DateField(verbose_name="Дата заезда")
    check_out = models.DateField(verbose_name="Дата выезда")
    adults = models.PositiveSmallIntegerField(default=1, verbose_name="Взрослые")
    children = models.PositiveSmallIntegerField(default=0, verbose_name="Дети")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая цена")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    # Архитектурный задел под онлайн-оплату
    payment_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ID платежа")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-created_at']

    def __str__(self):
        return f"Бронь #{self.id} – {self.room.name} ({self.check_in}–{self.check_out})"

    def calculate_total_price(self):
        """Вызывает метод комнаты для расчёта стоимости."""
        return self.room.get_current_price(self.check_in, self.check_out)

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)