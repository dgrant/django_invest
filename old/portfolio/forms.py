from django import forms
from django.forms.extras.widgets import SelectDateWidget

from .models import *

DATES = [x + 1995 for x in range(20)]

# class CreateEditTransactionForm:
#    date = forms.DateField(label='Date', widget=SelectDateWidget(years=tuple(DATES)))
#    type = forms.ChoiceField(label='Type', initial='buy', choices=Transaction.TRANSACTION_CHOICES)
#    shares = forms.IntegerField(label='Shares', required=False)
#    price = forms.FloatField(label='Price', required=False)
#    commission = forms.FloatField(label='Commission', required=False)
#    exchange_rate = forms.FloatField(label='Exchange Rate', required=False)
#    to_holding = forms.ModelChoiceField(queryset=Holding.objects.all(), label='Investment (to)', required=True)
#    from_holding = forms.ModelChoiceField(queryset=Holding.objects.all(), label='Source (from)', required=False)

# class HoldingForm(forms.ModelForm):
#    class Meta:
#        model = Holding
#        exclude = ('user',)
