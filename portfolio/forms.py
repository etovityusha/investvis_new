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
