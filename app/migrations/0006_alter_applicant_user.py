from django.db import migrations
from django.contrib.auth import get_user_model

User = get_user_model()  # This already points to your custom User model

def remove_invalid_applicants(apps, schema_editor):
    Applicant = apps.get_model('app', 'Applicant')
    
    # Ensure all users have at most one applicant record
    for user in User.objects.all():
        applicants = Applicant.objects.filter(user=user)  # 'user' is a User instance, not a string
        if applicants.count() > 1:
            # Keep the first applicant and remove the rest
            applicants[1:].delete()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_applicant_skills_jobpost_skills_alter_applicant_cv'),  
    ]

    operations = [
        migrations.RunPython(remove_invalid_applicants),
    ]
