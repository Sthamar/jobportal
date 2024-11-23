from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import User
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )
    )
    
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                'class':'form-control'
            }
        )
    )
    
    
    
class SignupForm(UserCreationForm):
    username = forms.CharField(
        
        widget = forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )
    )
    
    
    password1 = forms.CharField(
        label= 'Enter Password',
        widget = forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password1'
            }
        )
    )
    
   
    
    password2 = forms.CharField(
        label= 'Confirm Password',
        widget = forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password2'
            }
        )
    )
    
    
    
    class Meta:
        model = User
        fields = ('username', 'is_applicant','is_employer')
        
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username.isdigit():
            raise ValidationError("The username cannot consist of numbers only.")
        return username