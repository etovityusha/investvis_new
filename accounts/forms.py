from django import forms

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
        confirm_email = cleaned_data.get("confirm_email")
        bio = cleaned_data.get("bio")

        if email != confirm_email:
            raise forms.ValidationError(
                "Emails must match!"
            )