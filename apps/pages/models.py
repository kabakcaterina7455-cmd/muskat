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