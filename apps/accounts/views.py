from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Sum

from .forms import CustomUserCreationForm, ProfileEditForm
from .models import Profile
from apps.bookings.models import Booking


class RegisterView(View):
    """Регистрация."""
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('core:home')
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    """Вход в личный кабинет."""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:home')
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"С возвращением, {user.email}!")
            return redirect('core:home')

        messages.error(request, "Неверный email или пароль.")
        return render(request, 'accounts/login.html', {'email': email})

class LogoutView(View):
    """Выход из аккаунта."""

    def get(self, request):
        logout(request)
        return redirect('core:home')

    def post(self, request):
        logout(request)
        return redirect('core:home')


@login_required
def profile_view(request):
    """Личный кабинет со списком броней и статистикой."""
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    total_bookings = bookings.count()
    total_nights = sum(b.nights for b in bookings)
    total_spent = bookings.filter(status__in=['confirmed', 'completed']).aggregate(
        s=Sum('total_price')
    )['s'] or 0

    context = {
        'bookings': bookings,
        'total_bookings': total_bookings,
        'total_nights': total_nights,
        'total_spent': total_spent,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    """Редактирование профиля."""
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            user.save()

            profile.birth_date = form.cleaned_data['birth_date']
            if form.cleaned_data['avatar']:
                profile.avatar = form.cleaned_data['avatar']
            profile.save()

            messages.success(request, "Профиль обновлён!")
            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'birth_date': profile.birth_date,
        })

    return render(request, 'accounts/profile_edit.html', {'form': form, 'profile': profile})


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Смена пароля."""
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, "Пароль успешно изменён!")
        return response