from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Управление отзывами в админке."""
    list_display = ('id', 'room', 'user', 'rating', 'is_moderated', 'created_at')
    list_filter = ('is_moderated', 'rating', 'room')
    search_fields = ('text', 'user__email', 'room__name')
    list_editable = ('is_moderated',)
    readonly_fields = ('created_at',)
    actions = ['approve_reviews', 'reject_reviews']

    def approve_reviews(self, request, queryset):
        """Массово одобрить выбранные отзывы."""
        updated = queryset.update(is_moderated=True)
        self.message_user(request, f"Одобрено отзывов: {updated}")
    approve_reviews.short_description = "✅ Одобрить выбранные отзывы"

    def reject_reviews(self, request, queryset):
        """Снять одобрение с выбранных отзывов."""
        updated = queryset.update(is_moderated=False)
        self.message_user(request, f"Снято одобрение: {updated}")
    reject_reviews.short_description = "❌ Снять одобрение"
    