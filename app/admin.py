from django.contrib import admin
from app.models import Applicant, JobPost, Location
# Register your models here.

admin.site.register(Applicant)
admin.site.register(JobPost)
admin.site.register(Location)