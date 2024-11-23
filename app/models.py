from django.db import models
from django.conf import settings
from django.utils.text import slugify
from employer.models import Employer
from datetime import datetime
from django.core.validators import FileExtensionValidator

User = settings.AUTH_USER_MODEL
# Create your models here.

class Location(models.Model):
    city = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return f"{self.city} in {self.province}"
    
    
class JobPost(models.Model):
    JOB_TYPE_CHOICES = [
        ("Full Time", "Full Time"),
        ("Part Time", "Part Time"),
        ("Intern", "Intern"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    responsibility = models.TextField(null=True)
    qualification = models.TextField(null=True)
    date = models.DateTimeField(auto_now=True)
    expiry = models.DateField(null=True)
    vacancy = models.IntegerField(null=True)
    salary = models.IntegerField()
    slug = models.SlugField(null = True, max_length=40, unique=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True )
    type = models.CharField(max_length=200, null=False, choices=JOB_TYPE_CHOICES)
    company = models.CharField(max_length= 200,null=True)
    user = models.ForeignKey(Employer, on_delete=models.CASCADE, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:40]
            slug = base_slug
            counter = 1

            while JobPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)
              
    def __str__(self):
        return f"{self.title} with salary ${self.salary}"
    
    @property
    def is_expired(self):
        return datetime.now().date() >= self.expiry
    
    

class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE,blank=True, null=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=250)
    portfolio_link = models.URLField(null=True, blank=True)
    cv = models.FileField(upload_to='documents/', max_length=100,validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])])
    
    def __str__(self):
        return self.full_name
    