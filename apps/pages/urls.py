from django.urls import path
from .views import PageDetailView, ContactsView, GalleryView

app_name = 'pages'

urlpatterns = [
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('<slug:slug>/', PageDetailView.as_view(), name='page'),
]