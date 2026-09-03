from django.urls import path
from .views import ReviewCreateView

app_name = 'reviews'

urlpatterns = [
    path('create/<int:room_id>/', ReviewCreateView.as_view(), name='create'),
]