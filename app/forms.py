from django import forms
from app.models import Applicant, JobPost

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['full_name','email','portfolio_link', 'cv']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email'
            }),
            'portfolio_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Portfolio Website'
            }),
            'cv': forms.ClearableFileInput(attrs={
                'class': 'form-control bg-white',
            }),  
        }
        
        
class JobSearchForm(forms.Form):
    keyword = forms.CharField(
        max_length=100, 
        required=False, 
        label="Keyword",
        widget=forms.TextInput(attrs={
            'class': "form-control border-0",
            'placeholder': "Keyword"
        })
    )
    category = forms.ChoiceField(
        choices=[
            ('Full Time', 'Full Time'),
            ('Part Time', 'Part Time'),
            ('Intern', 'Intern'),
        ],
        required=False,
        label='Category',
        widget=forms.Select(attrs={
            'class': "form-control border-0",
            'placeholder': "Category"
        })
    )
    location = forms.CharField(
        max_length=100, 
        required=False, 
        label="Location",
        widget=forms.TextInput(attrs={
            'class': "form-control border-0",
            'placeholder': "Location"
        })
    )
    
        