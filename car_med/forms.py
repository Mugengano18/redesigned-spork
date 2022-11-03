from django import forms

from car_med.models import Retail_information


class Retail_info(forms.ModelForm):
    class Meta:
        model = Retail_information
        fields = ['fullname', 'company_name']
