from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'rating', 'is_moderated')
    list_filter = ('is_moderated', 'rating')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_moderated=True)
    approve_reviews.short_description = "Одобрить отзывы"