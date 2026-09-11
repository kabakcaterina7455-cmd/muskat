from django.views.generic import TemplateView, ListView
from apps.rooms.models import Room, Service
from apps.reviews.models import Review
from apps.pages.models import Page, GalleryImage


class HomeView(TemplateView):
    """Главная страница."""
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.filter(is_active=True)[:4]
        context['reviews'] = Review.objects.filter(is_moderated=True).order_by('-created_at')[:3]
        context['services'] = Service.objects.filter(is_active=True)[:4]
        return context


class ServiceListView(ListView):
    """Страница со всеми услугами."""
    model = Service
    template_name = 'core/services.html'
    context_object_name = 'services'
    queryset = Service.objects.filter(is_active=True)


    



class ForKidsView(TemplateView):
    """Страница «Для детей»."""
    template_name = 'core/for_kids.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Текст страницы из админки (если создана Page со slug='for-kids')
        try:
            context['page'] = Page.objects.get(slug='for-kids', is_active=True)
        except Page.DoesNotExist:
            context['page'] = None

        # Фото из галереи (категория «Для детей»)
        context['kids_photos'] = GalleryImage.objects.filter(
            category__slug='kids',
            is_active=True
        )[:8]

        return context