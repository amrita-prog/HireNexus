from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import StudentSignUpForm, RecruiterSignUpForm
from django.contrib.auth import login, logout, authenticate 
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from jobs.models import Job, Application
from django.db.models import Count


def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST, request.FILES) # files for image upload
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Student account created successfully.")
            return redirect('student_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentSignUpForm()
    return render(request, 'accounts/signup.html', {'form_data': form,'user_type':'Student'})



def recruiter_signup(request):
    if request.method == 'POST':
        form = RecruiterSignUpForm(request.POST, request.FILES) # files for image upload
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Recruiter account created successfully.")
            return redirect('recruiter_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RecruiterSignUpForm()
    return render(request, 'accounts/signup.html', {'form_data': form,'user_type':'Recruiter'})


def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = CustomUser.objects.get(email=email)
            user = authenticate(request,username=user_obj.email,password=password)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            login(request,user)
            if user.roles == 'student':
                messages.success(request, "Logged in successfully as Student.")
                return redirect('student_dashboard')
            elif user.roles == 'recruiter':
                messages.success(request, "Logged in successfully as Recruiter.")
                return redirect('recruiter_dashboard')
            else:
                return redirect('admin:index')
            
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'accounts/login.html')

@login_required
def recruiter_dashboard(request):
    user = request.user
    jobs = Job.objects.filter(posted_by=user)
    total_jobs = Job.objects.count()
    total_applications = Application.objects.filter(job__posted_by = request.user).count()

    job_type_data = (
        Job.objects.values('job_type').annotate(count=Count('job_type')).order_by('-count')
    )
    most_applied_jobs = (
        jobs.annotate(app_count=Count('application'))
        .order_by('-app_count').first()
    )
    chart_label = [item['job_type'] for item in job_type_data]
    chart_data = [item['count'] for item in job_type_data]

    return render(request, 'accounts/recruiter_dashboard.html', {
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'most_applied_jobs': most_applied_jobs,
        'chart_label': chart_label,
        'chart_data': chart_data,
    })

@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')


@login_required
def student_dashboard(request):
    user = request.user
    total_jobs = Job.objects.count()
    jobs_applied = Application.objects.filter(student=user).count()
    job_type_data = (
        Job.objects.values('job_type').annotate(count=Count('job_type')).order_by('-count')
    )

    applications = Application.objects.filter(student = request.user)
    unseen_count = applications.filter(status_notified=True).exclude(status='applied').count()

    chart_label = [item['job_type'] for item in job_type_data]
    chart_data = [item['count'] for item in job_type_data]
        
    return render(request, 'accounts/student_dashboard.html',{
        'total_jobs': total_jobs,
        'jobs_applied': jobs_applied,
        'chart_label': chart_label,
        'chart_data': chart_data,
        'applications': applications,
        'unseen_count': unseen_count,
    })


@login_required
def student_applied_jobs(request):
    applications = Application.objects.filter(student=request.user)
    applications.filter(status_notified=True).exclude(status='applied').update(status_notified=False)
    return render(request, 'accounts/student_applied_jobs.html', {'applications': applications})