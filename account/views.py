from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from account.forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def register(request):
    msg = ''
    try:    
        if request.method == "POST":
            form = SignupForm(request.POST)
            
            if form.is_valid():
                applicant = request.POST.get("is_applicant")
                employer = request.POST.get("is_employer")
                print(f'applicant: {applicant} employer: {employer}')
                if applicant == 'on' and employer == "on":
                    msg = 'select only one role'
                elif applicant == None and employer == None:
                    msg = 'select altest one role'
                else:
                    try:
                        user = form.save()
                        msg = 'user created'
                        return redirect('login_view')
                    except Exception as e:
                        msg=f'Error creating user: {str(e)}'
            else:
                msg = ''
        else:
            form = SignupForm()
    except Exception as e:
        msg = f'something went wrong: {str(e)}'
    return render(request, 'registration.html', {'form':form, 'msg':msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = "Welcome"
    try:
        if request.method == 'POST':
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                try:
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        if user.is_applicant:
                            return redirect('home')
                        if user.is_employer:
                            return redirect('index')
                        if user.is_admin:
                            return render(request, 'login.html', {'form':form, 'msg':"Login failed. This user cannot login here"})
                    else:
                        msg = 'Username or password is incorrect'
                except Exception as e:
                    msg = f'Authentication error: {str(e)}'
            else:
                form = LoginForm()
    except Exception as e:
        msg = f'An error occurred: {str(e)}'
    return render(request, 'login.html', {'form':form, 'msg':msg})


def logoutuser(request):
    try:
        if request.method == 'POST':
            logout(request)  
            return redirect('home')  
        else:
            return HttpResponse('Invalid request method', status=405) 
    except Exception as e:
        return HttpResponse(f'An error occurred while logging out: {str(e)}', status=500)


            
def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')