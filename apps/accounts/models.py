from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Кастомная модель пользователя: вход по email.
    """
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")

    USERNAME_FIELD = 'email'          # вход по email
    REQUIRED_FIELDS = ['username']    # username всё ещё требуется

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
    Расширенный профиль пользователя.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    preferences = models.JSONField(default=dict, blank=True, verbose_name="Предпочтения")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Профиль {self.user.email}"