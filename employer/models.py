from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    company_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=250)
    website = models.URLField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    
    def __str__(self):
        return self.company_name
    

    
    
