
from django.views.generic import TemplateView
from apps.rooms.models import Room, Service
from apps.reviews.models import Review

class HomeView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.filter(is_active=True)[:4]
        context['reviews'] = Review.objects.filter(is_moderated=True).order_by('-created_at')[:3]
        context['services'] = Service.objects.filter(is_active=True)[:4]
        return context
