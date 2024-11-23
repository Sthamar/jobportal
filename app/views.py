from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from app.forms import JobSearchForm, ApplicantForm
from app.models import JobPost, Applicant
from datetime import datetime

# Create your views here.


#homepage view
def home(request):
    job_post = JobPost.objects.all().order_by('-date')
    search = JobSearchForm(request.GET or None)
    full_time = job_post.filter(type='Full Time')
    part_time = job_post.filter(type='Part Time')
    intern = job_post.filter(type='Intern')
    
    
    if request.method == "GET" and search.is_valid():
         return redirect('search', keyword=search.cleaned_data['keyword'], 
                        category=search.cleaned_data['category'], 
                        location=search.cleaned_data['location'])
        
    
          
    context = {"job_post":job_post, "full_time":full_time, "part_time":part_time,"intern": intern, 'search':search}
    return render(request, 'app/home.html',context)


def search_list(request):
    matched_jobs = JobPost.objects.filter(expiry__gte = datetime.now().date())
    keyword = request.GET.get('keyword')
    category = request.GET.get('category')
    location = request.GET.get('location')
    print(keyword)
    form = JobSearchForm(request.GET or None)  
        
    if keyword:
            matched_jobs = matched_jobs.filter(
                Q(title__icontains = keyword) | Q(description__icontains = keyword)
            )
         
    if category:
        matched_jobs = matched_jobs.filter(
            type = category
        )
        
            
    if location:
        matched_jobs = matched_jobs.filter(
                Q(location__city__icontains=location) |
                Q(location__province__icontains=location) |
                Q(location__country__icontains=location)
            )
        
    context = {
        'form': form,
        'matched_jobs': matched_jobs,
        'search': form  # Using the same form object
    }
    
    return render(request, 'app/search_list.html', context)


def detail_page(request, slug):
    try:
        job = get_object_or_404(JobPost, slug=slug)
        already_applied =  Applicant.objects.filter(user = request.user, job_post = job).exists()
        form = ApplicantForm(request.POST, request.FILES)
        context = {"job": job, "form": form,'success': True, 'applied':already_applied }
        if already_applied:
            return render(request, 'app/details.html', context)
        elif request.method == 'POST':
            if form.is_valid():
                newapplicant = form.save(commit=False)
                newapplicant.user = request.user 
                newapplicant.job_post = job
                newapplicant.save()
                return redirect('detail_page', slug = slug)
            else:
                print("Form errors:", form.errors)  # This will show which field is causing issues
                print("CV field errors:", form.errors.get('cv'))
        else:
            form = ApplicantForm()  # Create a new form instance for GET requests
    except:
        return redirect('login_view')

    context = {"job": job, "form": form}
    return render(request, 'app/details.html', context)