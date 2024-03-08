# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UpdateQuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    card_number = forms.IntegerField()
    cvv = forms.IntegerField()



    