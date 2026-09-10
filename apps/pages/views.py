from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, TemplateView
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Page
from django.views.generic import ListView
from .models import GalleryImage, GalleryCategory

class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/page_detail.html'
    context_object_name = 'page'

class ContactsView(TemplateView):
    template_name = 'pages/contacts.html'

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and email and message:
            send_mail(
                subject=f"Сообщение от {name}",
                message=f"От: {email}\n\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.MANAGER_EMAIL],
                fail_silently=True,
            )
            messages.success(request, "Сообщение отправлено!")
        else:
            messages.error(request, "Заполните все поля.")
        return redirect('pages:contacts')

        


class GalleryView(ListView):
    model = GalleryImage
    template_name = 'pages/gallery.html'
    context_object_name = 'images'
    queryset = GalleryImage.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = GalleryCategory.objects.all()
        slug = self.request.GET.get('category')
        if slug:
            context['selected_category'] = slug
            context['images'] = self.queryset.filter(category__slug=slug)
        return context