from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from apps.rooms.models import Room

class Review(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка", choices=[(i, i) for i in range(1, 6)])
    is_moderated = models.BooleanField(default=False, verbose_name="Одобрено")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв {self.user.email} о {self.room.name}"