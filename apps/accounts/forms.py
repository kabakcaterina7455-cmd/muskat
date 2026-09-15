from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации."""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Подтверждение пароля")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileEditForm(forms.Form):
    """Форма редактирования профиля: User + Profile."""
    first_name = forms.CharField(
        max_length=150, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Имя"
    )
    last_name = forms.CharField(
        max_length=150, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Фамилия"
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Email"
    )
    phone = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Телефон"
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label="Аватар"
    )
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Дата рождения"
    )