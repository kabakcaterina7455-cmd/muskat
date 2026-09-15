from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView,
    profile_view, profile_edit_view, CustomPasswordChangeView,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),    # ← наш LoginView
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='password_change'),
]