from stock.models import Stock
from django import forms


class CompanyCreateForm(forms.ModelForm):
    ticker = forms.TextInput()
    currency = forms.Select()

    class Meta:
        model = Stock
        fields = ('ticker', 'currency',)
