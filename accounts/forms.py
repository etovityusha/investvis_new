from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватар')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Имя', required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Фамилия', required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    birth_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Дата рождения',
                                 required=False)
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='О себе', required=False)
    open_portfolio = forms.BooleanField(label='Открытый портфель', required=False)

    class Meta:
        model = models.Profile
        exclude = ('user', )


class UserRegisterForms(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailInput()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)