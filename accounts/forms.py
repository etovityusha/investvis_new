from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватар')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Имя')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Фамилия')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Город')
    birth_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Дата рождения')
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Страна')
    confirm_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Подтвердите email')
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='О себе')
    open_portfolio = forms.BooleanField(label='Открытый портфель')

    class Meta:
        model = models.Profile
        exclude = ('user', )

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        email = cleaned_data.get("email")
        bio = cleaned_data.get("bio")


class UserRegisterForms(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailInput()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)