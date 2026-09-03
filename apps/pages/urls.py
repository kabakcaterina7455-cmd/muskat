from django.urls import path
from .views import PageDetailView, ContactsView

app_name = 'pages'

urlpatterns = [
    path('<slug:slug>/', PageDetailView.as_view(), name='page'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]