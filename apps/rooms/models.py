from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify

class Amenity(models.Model):
    """Удобства в номере (Wi‑Fi, кондиционер и т.п.)"""
    name = models.CharField(max_length=100, verbose_name="Название")
    icon = models.CharField(max_length=50, blank=True, help_text="Класс FontAwesome, например 'fa-wifi'")

    class Meta:
        verbose_name = "Удобство"
        verbose_name_plural = "Удобства"

    def __str__(self):
        return self.name


class Room(models.Model):
    """Модель номера."""
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="ЧПУ")
    description = models.TextField(verbose_name="Полное описание")
    short_description = models.CharField(max_length=300, verbose_name="Краткое описание")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Базовая цена за сутки")
    max_adults = models.PositiveSmallIntegerField(default=2, verbose_name="Макс. взрослых")
    max_children = models.PositiveSmallIntegerField(default=1, verbose_name="Макс. детей")
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="Количество номеров")
    square = models.PositiveSmallIntegerField(verbose_name="Площадь, м²")
    bed_type = models.CharField(max_length=100, verbose_name="Тип кровати")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    amenities = models.ManyToManyField(Amenity, blank=True, verbose_name="Удобства")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ['price_per_night']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_current_price(self, check_in, check_out):
        """
        Рассчитывает итоговую стоимость за период с учётом сезонных цен.
        """
        from datetime import timedelta
        base = self.price_per_night
        total = 0
        current = check_in
        while current < check_out:
            seasonal = self.seasonal_prices.filter(date_from__lte=current, date_to__gte=current).first()
            price = seasonal.price if seasonal else base
            total += price
            current += timedelta(days=1)
        return total

    @property
    def reviews_count(self):
        """Количество одобренных отзывов."""
        return self.reviews.filter(is_moderated=True).count()

    @property
    def average_rating(self):
        """Средний рейтинг на основе одобренных отзывов. Возвращает None, если отзывов нет."""
        reviews = self.reviews.filter(is_moderated=True)
        if not reviews.exists():
            return None
        total = sum(r.rating for r in reviews)
        return round(total / reviews.count(), 1)    


class RoomImage(models.Model):
    """Фотографии номера."""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='rooms/', verbose_name="Фото")
    is_main = models.BooleanField(default=False, verbose_name="Основное фото")

    class Meta:
        verbose_name = "Фото номера"
        verbose_name_plural = "Фото номеров"

    def __str__(self):
        return f"Фото для {self.room.name}"


class SeasonalPrice(models.Model):
    """Сезонная цена для номера на период."""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='seasonal_prices')
    date_from = models.DateField(verbose_name="Начало")
    date_to = models.DateField(verbose_name="Конец")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за сутки")

    class Meta:
        verbose_name = "Сезонная цена"
        verbose_name_plural = "Сезонные цены"
        ordering = ['date_from']

    def __str__(self):
        return f"{self.room.name}: {self.date_from}–{self.date_to} = {self.price}"


class Service(models.Model):
    """Дополнительные услуги (трансфер, SUP, экскурсии и т.д.)"""
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,             # ← можно не указывать
        verbose_name="Цена (₽)"
    )
    price_note = models.CharField(
        max_length=100, blank=True,
        verbose_name="Текст цены (если не число)",
        help_text="Например: «по запросу», «от 500 ₽», «бесплатно». "
                  "Если заполнено — показывается вместо числа."
    )
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_price_display(self):
        """Возвращает правильный текст цены: либо price_note, либо число."""
        if self.price_note:
            return self.price_note
        if self.price is not None:
            # Красиво без .00
            if self.price == int(self.price):
                return f"{int(self.price)} ₽"
            return f"{self.price} ₽"
        return ""

    def __str__(self):
        return self.name