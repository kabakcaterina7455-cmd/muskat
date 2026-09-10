from django.db import models

# Create your models here.
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Page(models.Model):
    slug = models.SlugField(max_length=200, unique=True, verbose_name="ЧПУ")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = RichTextUploadingField(verbose_name="Содержание")
    seo_title = models.CharField(max_length=200, blank=True, verbose_name="SEO-заголовок")
    seo_description = models.TextField(max_length=500, blank=True, verbose_name="SEO-описание")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"

    def __str__(self):
        return self.title

from django.utils.text import slugify


class GalleryCategory(models.Model):
    """Категория для галереи (Территория, Номера, Для детей и т.д.)"""
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="ЧПУ")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Категория галереи"
        verbose_name_plural = "Категории галереи"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    """Фотография в галерее."""
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='images',
        verbose_name="Категория"
    )
    title = models.CharField(max_length=200, blank=True, verbose_name="Подпись")
    image = models.ImageField(upload_to='gallery/', verbose_name="Фото")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Фото галереи"
        verbose_name_plural = "Фото галереи"

    def __str__(self):
        return self.title or f"Фото #{self.id}"        