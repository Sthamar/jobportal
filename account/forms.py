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
    USER_TYPE_CHOICES = [
        ('applicant', 'Applicant'),
        ('employer', 'Employer'),
    ]
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    password1 = forms.CharField(
        label='Enter Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password1'})
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password2'})
    )
    
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="user type"
    )

    class Meta:
        model = User
        fields = ('username',)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username.isdigit():
            raise ValidationError("The username cannot consist of numbers only.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")
    
        if not user_type:
            raise ValidationError("Please select a user type.")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_applicant = self.cleaned_data['user_type'] == 'applicant'
        user.is_employer = self.cleaned_data['user_type'] == 'employer'
        if commit:
            user.save()
        return user
