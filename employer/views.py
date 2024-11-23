from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from app.views import JobPost, Applicant
from app.forms import JobSearchForm
from employer.forms import CreateJob
from employer.models import Employer
# Create your views here.

    
    
def index(request):
    if request.user.is_authenticated:
        if Employer.objects.filter(user=request.user).exists():
            employer = Employer.objects.get(user=request.user)
            job = JobPost.objects.filter(user=employer)

            full_time = job.filter(type='Full Time')
            part_time = job.filter(type='Part Time')
            intern = job.filter(type='Intern')
                
            context = {"job_post":job, "full_time":full_time, "part_time":part_time,"intern": intern,}
            return render(request, 'employer/index.html',context)
        else:
            return render(request, 'employer/index.html',{'msg':'no jobs'})
    else:
        return redirect('home')




def create_job(request):
    msg = ''
    if request.method == 'POST':
        form = CreateJob(request.POST, user=request.user)
        try:
            if form.is_valid():
                form.save(user=request.user)
                return redirect('thank') 
            else:
                msg = "There were errors in the form. Please fix them and try again."
        except Exception as e:
            msg = f"Error creating job post: {str(e)}"
    else:
        form = CreateJob() 

    context = {'form': form, 'msg': msg}
    return render(request, 'employer/create_job.html', context)


def thank(request):
    return render(request, 'employer/thankyou.html', )


def edit_page(request, slug):
    job = get_object_or_404(JobPost, slug=slug)
    if request.method == "POST":
        form = CreateJob(request.POST, instance=job, user=request.user)
        if form.is_valid():
            form.save(user=request.user)
            
            return redirect('index')
    else:
        form = CreateJob(instance=job, user=request.user)  # Pass the user here

    return render(request, 'employer/edit_page.html', {'form': form, 'job':job})


def delete_job(request, slug):
    job = get_object_or_404(JobPost, slug=slug,)
    job.user = Employer.objects.get(user=request.user)
    if request.method == "POST":
       job.delete() 
       return redirect('index')
    return render(request, 'employer/thankyou.html')

        
        
def applicant_list(request, slug):
    job = get_object_or_404(JobPost, slug=slug)
    applicants = Applicant.objects.filter(job_post= job)
    for applicant in applicants:
        print(applicant.user.username)

    # Pass the job and applicants to the template
    return render(request, 'employer/applicants.html', {
        'job': job,
        'applicants': applicants,
    })


def applicant_detail(request,slug,id):
    job = get_object_or_404(JobPost, slug=slug)
    applicant = get_object_or_404(Applicant,id=id)
    full_name = applicant.full_name.split()[0]
    return render(request, 'employer/applicant_detail.html',{
        'job':job,
        'applicant':applicant,
        'full_name':full_name
        
    })