from django import forms
from .models import Activation
from crispy_forms.helper import FormHelper
from django.forms import ModelForm
from django.core.validators import RegexValidator


class ActivationForm(forms.ModelForm):
   
   cell_number = forms.CharField(max_length=10, validators=[RegexValidator(
        '^(\+27|0)[6-8][0-9]{8}$', message="Enter a Valid South African Phone Number")])
 
   class Meta:
      model=Activation
      fields=('voucher_type','cell_number',)

      
