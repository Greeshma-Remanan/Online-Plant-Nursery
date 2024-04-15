from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#Register
class Register(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','password1','password2']
#Login
class Login(forms.Form):
    username=forms.CharField()
    password=forms.CharField()


#Address 

class OrderForm(forms.Form):
    address=forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","placeholder":"address","rows":5}))