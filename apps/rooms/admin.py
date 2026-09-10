from django.contrib import admin
from django.utils.html import format_html
from .models import Room, RoomImage, SeasonalPrice, Amenity, Service


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 3
    fields = ('image', 'is_main', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "Нет фото"
    preview.short_description = "Превью"


class SeasonalPriceInline(admin.TabularInline):
    model = SeasonalPrice
    extra = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_night', 'quantity', 'is_active')   # ← добавили quantity
    list_filter = ('is_active', 'amenities')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [RoomImageInline, SeasonalPriceInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'short_description')
        }),
        ('Цены и вместимость', {
            'fields': ('price_per_night', 'max_adults', 'max_children', 'quantity')  # ← добавили
        }),
        ('Характеристики', {
            'fields': ('square', 'bed_type', 'amenities')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SeasonalPrice)
class SeasonalPriceAdmin(admin.ModelAdmin):
    list_display = ('room', 'date_from', 'date_to', 'price')
    list_filter = ('room',)