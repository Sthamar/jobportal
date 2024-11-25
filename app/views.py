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
        
    
          
    context = {"job_post":job_post, "full_time":full_time, "part_time":part_time,"intern": intern, 'search':search, "user": request.user}
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



def recommend_jobs(applicant_skills):
    if not applicant_skills:
        return [] 
    
    job_posts = JobPost.objects.all()
    recommended_jobs = []

    
    applicant_skills_set = set(skill.lower() for skill in applicant_skills.split(","))

    for job in job_posts:
        if job.skills:
            job_skills = job.skills.split(",")
            job_skills_set = set(skill.lower() for skill in job_skills)
        
            match_score = len(applicant_skills_set.intersection(job_skills_set))

            if match_score > 0:
                recommended_jobs.append((job, match_score))
                
    print('hello')
    
    # Sort jobs by the match score in descending order
    recommended_jobs.sort(key=lambda x: x[1], reverse=True)
    print(recommended_jobs)
    
    return recommended_jobs


def detail_page(request, slug):
    try:
        job = get_object_or_404(JobPost, slug=slug)
        already_applied =  Applicant.objects.filter(user = request.user, job_post = job).exists()
        form = ApplicantForm(request.POST, request.FILES)
        applicant = Applicant.objects.filter(user=request.user, job_post =job).first()
            
        if applicant:
            applicant_skills = applicant.skills
        else:
            applicant_skills = ''
            
        recommended_jobs = recommend_jobs(applicant_skills)
        
        context = {"job": job, "form": form,'success': True, 'applied':already_applied, 'recommended_jobs':recommended_jobs }
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
                print("Form errors:", form.errors)  
                print("CV field errors:", form.errors.get('cv'))
        else:
            form = ApplicantForm()  
    except Exception as e:
        # If there’s an error, redirect to login page
        print(f"Error: {e}")
        return redirect('login_view')

    context = {"job": job, "form": form}
    return render(request, 'app/details.html', context)