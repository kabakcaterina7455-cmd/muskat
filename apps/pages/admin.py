from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.core.files.base import File
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Page, GalleryCategory, GalleryImage


# ========================================
# Кастомный виджет и поле для multiple-загрузки
# ========================================
class MultipleFileInput(forms.FileInput):
    """Виджет, который разрешает выбирать несколько файлов сразу."""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Поле, которое принимает список файлов."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'multiple': True, 'class': 'form-control'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


# ========================================
# Страницы (Page)
# ========================================
class PageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Page
        fields = '__all__'


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    list_display = ('title', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


# ========================================
# Галерея (категории)
# ========================================
@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}


# ========================================
# Галерея (фото) — с массовой загрузкой
# ========================================
class MultipleImageUploadForm(forms.Form):
    """Форма для загрузки нескольких фото сразу."""
    category = forms.ModelChoiceField(
        queryset=GalleryCategory.objects.all(),
        label="Категория",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    images = MultipleFileField(
        label="Выберите фотографии (можно несколько сразу)",
        required=True
    )
    is_active = forms.BooleanField(
        initial=True,
        required=False,
        label="Активны",
        widget=forms.CheckboxInput()
    )


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'order', 'is_active', 'preview')
    list_filter = ('category', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title',)
    readonly_fields = ('preview',)
    change_list_template = 'admin/galleryimage_changelist.html'

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit: cover;" />',
                obj.image.url
            )
        return "—"
    preview.short_description = "Превью"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('bulk-upload/', self.admin_site.admin_view(self.bulk_upload_view),
                 name='pages_galleryimage_bulk_upload'),
        ]
        return custom_urls + urls

    def bulk_upload_view(self, request):
        from django.shortcuts import render, redirect
        from django.contrib import messages

        if request.method == 'POST':
            form = MultipleImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                category = form.cleaned_data['category']
                is_active = form.cleaned_data['is_active']
                files = form.cleaned_data['images']
                count = 0
                for f in files:
                    img = GalleryImage(
                        category=category,
                        title=f.name.rsplit('.', 1)[0],
                        is_active=is_active,
                    )
                    img.image.save(f.name, File(f), save=True)
                    count += 1
                messages.success(request, f"Успешно загружено {count} фото в категорию «{category.name}».")
                return redirect('admin:pages_galleryimage_changelist')
        else:
            form = MultipleImageUploadForm()

        context = {
            **self.admin_site.each_context(request),
            'title': 'Массовая загрузка фотографий',
            'form': form,
            'opts': self.model._meta,
        }
        return render(request, 'admin/bulk_upload.html', context)