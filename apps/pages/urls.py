
from django.urls import path
from .views import PageDetailView, ContactsView, GalleryView, FAQView

app_name = 'pages'

urlpatterns = [
    # Конкретные пути — идут ПЕРВЫМИ
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('faq/', FAQView.as_view(), name='faq'),
    
    # Общий slug — идёт ПОСЛЕДНИМ
    path('<slug:slug>/', PageDetailView.as_view(), name='page'),
]