from django import forms
from app.models import JobPost
from employer.models import Employer


class CreateJob(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Company Email'
        })
    )
    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Company Website (optional)'
        })
    )
    contact_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contact Number (optional)'
        })
    )

    class Meta:
        model = JobPost
        fields = ['title', 'description', 'responsibility', 'qualification', 'expiry', 'vacancy', 'salary', 'location', 'type', 'company']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Job Description'
            }),
            'responsibility': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Responsibilities'
            }),
            'qualification': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Qualifications'
            }),
            'expiry': forms.DateInput(
                    attrs={
                        'class': 'form-control',
                        'type': 'date',
                        'placeholder': 'Expiry date'
                    },
                    ),
            'vacancy': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of Vacancies'
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Salary Amount'
            }),
            'location': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Job Location'
            }),
            'type': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Job Type'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Name'
            }),
        }

    def __init__(self, *args, **kwargs):
        # Extract user instance from the kwargs if provided
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # If user is provided, try to pre-populate employer fields
        if self.user:
            employer = Employer.objects.filter(user=self.user).first()
            if employer:
                self.fields['email'].initial = employer.email
                self.fields['website'].initial = employer.website
                self.fields['contact_number'].initial = employer.contact_number

    def save(self, user, *args, **kwargs):
        # Create or update Employer instance
        employer_data = {
            'email': self.cleaned_data['email'],
            'website': self.cleaned_data.get('website'),
            'contact_number': self.cleaned_data.get('contact_number')
        }

        # Get or create Employer instance
        employer, created = Employer.objects.get_or_create(user=user, defaults=employer_data)

        # Update the existing Employer instance if necessary
        if not created:
            for key, value in employer_data.items():
                setattr(employer, key, value)
            employer.save()

        # Create JobPost instance
        job_post = super().save(commit=False)
        job_post.user = employer
        job_post.save()

        return job_post
