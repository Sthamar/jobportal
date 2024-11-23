from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_applicant = models.BooleanField('Is applicant', default=False)
    is_employer = models.BooleanField('Is employer', default=False)