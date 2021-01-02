from django import forms

from datetime import datetime

from portfolio.models import BrokerReport, Deal


class BrokerReportForm(forms.ModelForm):
    report = forms.FileField(label='Выберите отчёт')

    class Meta:
        model = BrokerReport
        fields = ('broker', 'report')
        widgets = {
            'broker': forms.Select(attrs={'class': 'form-control'}),
        }


class DealCreateForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}), initial=datetime.now, label='Дата')
    transaction_type = forms.Select()
    ticker = forms.Select()
    price = forms.DecimalField(label='Цена за ед.', widget=forms.TimeInput(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(label='Количество', widget=forms.TimeInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Deal
        fields = ('date', 'transaction_type', 'ticker', 'price',  'quantity',)
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'ticker': forms.Select(attrs={'class': 'form-control'}),
        }
