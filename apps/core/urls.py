from django.urls import path
from .views import HomeView, ServiceListView, ForKidsView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('services/', ServiceListView.as_view(), name='services'),
    path('for-kids/', ForKidsView.as_view(), name='for_kids'),
]