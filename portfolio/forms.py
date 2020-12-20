from datetime import datetime

from django import forms
from . import models


class BrokerReportForm(forms.ModelForm):
    report = forms.FileField(label='Выберите отчёт')

    class Meta:
        model = models.BrokerReport
        fields = ('broker', 'report')
        widgets = {
            'broker': forms.Select(attrs={'class': 'form-control'}),
        }


class DealCreateForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}), initial=datetime.now, label='Дата')
    time = forms.TimeField(initial=datetime.now, label='Время', widget=forms.TimeInput(attrs={'class': 'form-control'}))
    transaction_type = forms.Select()
    ticker = forms.Select()
    price = forms.DecimalField(label='Цена за ед.', widget=forms.TimeInput(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(label='Количество', widget=forms.TimeInput(attrs={'class': 'form-control'}))
    fee = forms.DecimalField(label='Комиссия', widget=forms.TimeInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.Deal
        fields = ('date', 'time', 'transaction_type', 'ticker', 'price',  'quantity',  'fee')
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'ticker': forms.Select(attrs={'class': 'form-control'}),
        }
