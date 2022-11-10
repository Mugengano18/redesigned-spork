from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from car_med.models import Retail_information


class Retail_info(forms.ModelForm):
    class Meta:
        model = Retail_information
        fields = ['fullname', 'company_name']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
