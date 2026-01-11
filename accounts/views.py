from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import StudentSignUpForm, RecruiterSignUpForm, ProfileEditForm
from django.contrib.auth import login, logout, authenticate 
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from jobs.models import Job, Application
from django.db.models import Count, Q


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
    
    # Get recent applications for the recruiter
    recent_applications = Application.objects.filter(job__posted_by=user).select_related('job', 'student').order_by('-applied_at')[:5]
    
    chart_label = [item['job_type'] for item in job_type_data]
    chart_data = [item['count'] for item in job_type_data]

    return render(request, 'accounts/recruiter_dashboard.html', {
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'most_applied_jobs': most_applied_jobs,
        'chart_label': chart_label,
        'chart_data': chart_data,
        'recent_applications': recent_applications,
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

    chart_label = [item['job_type'] for item in job_type_data]
    chart_data = [item['count'] for item in job_type_data]

    # Get application status distribution
    applications = Application.objects.filter(student=user).select_related('job').order_by('-applied_at')
    status_data = applications.values('status').annotate(count=Count('status')).order_by('-count')
    
    # Map status codes to display names
    status_mapping = {
        'applied': 'Applied',
        'shortlisted': 'Shortlisted',
        'intervie_1': 'L1 Cleared',
        'interview_technical': 'Technical Cleared',
        'hr_cleared': 'HR Cleared',
        'rejected': 'Rejected',
        'offered': 'Offered',
        'hold': 'On Hold'
    }
    
    status_labels = [status_mapping.get(item['status'], item['status']) for item in status_data]
    status_counts = [item['count'] for item in status_data]

    recent_jobs = applications[:5]  # Get last 5 applications

    unseen_updates = (
        applications.filter(status_notified=True).exclude(status='applied').order_by('-applied_at')
    )        

    unseen_count = unseen_updates.count()
    latest_updates = unseen_updates

    return render(request, 'accounts/student_dashboard.html',{
        'total_jobs': total_jobs,
        'jobs_applied': jobs_applied,
        'chart_label': chart_label,
        'chart_data': chart_data,
        'status_labels': status_labels,
        'status_counts': status_counts,
        'applications': applications,
        'recent_jobs': recent_jobs,
        
        # notifications
        'unseen_count': unseen_count,
        'latest_updates': latest_updates,
    })


@login_required
def student_applied_jobs(request):
    applications = Application.objects.filter(student=request.user)
    applications.filter(status_notified=True).exclude(status='applied').update(status_notified=False)
    return render(request, 'accounts/student_applied_jobs.html', {'applications': applications})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            if user.roles == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('recruiter_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileEditForm(instance=user, user=user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def recruiter_applications(request):
    """View all applications for recruiter's jobs"""
    user = request.user
    if user.roles != 'recruiter':
        redirect('student_dashboard')
    
    # Get all applications for this recruiter's jobs
    applications = Application.objects.filter(job__posted_by=user).select_related('job', 'student').order_by('-applied_at')
    
    return render(request, 'accounts/recruiter_applications.html', {
        'applications': applications
    })

@login_required
def recruiter_reports(request):
    """Reports page for recruiter with analytics and insights"""
    user = request.user
    if user.roles != 'recruiter':
        return redirect('student_dashboard')
    
    # Get all jobs and applications for this recruiter
    jobs = Job.objects.filter(posted_by=user)
    applications = Application.objects.filter(job__posted_by=user).select_related('job', 'student')
    
    # 1. Application Funnel Data (Pipeline)
    status_mapping = {
        'applied': 'Applied',
        'shortlisted': 'Shortlisted',
        'intervie_1': 'L1 Interview',
        'interview_technical': 'Technical',
        'hr_cleared': 'HR Cleared',
        'offered': 'Offered',
        'rejected': 'Rejected',
        'hold_on': 'On Hold'
    }
    
    funnel_data = applications.values('status').annotate(count=Count('status')).order_by('status')
    funnel_labels = [status_mapping.get(item['status'], item['status']) for item in funnel_data]
    funnel_counts = [item['count'] for item in funnel_data]
    
    # Create combined list for easier template iteration
    funnel_combined = list(zip(funnel_labels, funnel_counts))
    
    # 2. Job Performance Data
    job_performance = jobs.annotate(
        total_applications=Count('application'),
        shortlisted_count=Count('application', filter=Q(application__status='shortlisted')),
        offered_count=Count('application', filter=Q(application__status='offered')),
        rejected_count=Count('application', filter=Q(application__status='rejected'))
    ).values('title', 'salary', 'job_type', 'created_at', 'total_applications', 'shortlisted_count', 'offered_count', 'rejected_count')
    
    # 3. Filter options
    date_filter = request.GET.get('date_filter', 'all')
    job_type_filter = request.GET.get('job_type', 'all')
    status_filter = request.GET.get('status', 'all')
    
    filtered_applications = applications
    
    # Apply filters
    if date_filter == 'this_month':
        from datetime import datetime
        current_month = datetime.now().month
        current_year = datetime.now().year
        filtered_applications = filtered_applications.filter(applied_at__month=current_month, applied_at__year=current_year)
    elif date_filter == 'last_3_months':
        from datetime import datetime, timedelta
        three_months_ago = datetime.now() - timedelta(days=90)
        filtered_applications = filtered_applications.filter(applied_at__gte=three_months_ago)
    
    if job_type_filter != 'all':
        filtered_applications = filtered_applications.filter(job__job_type=job_type_filter)
    
    if status_filter != 'all':
        filtered_applications = filtered_applications.filter(status=status_filter)
    
    # 6. Detailed Report Table (filtered)
    detailed_report = filtered_applications.select_related('job', 'student').order_by('-applied_at')
    
    # Get unique job types and statuses for filter dropdowns
    job_types = jobs.values_list('job_type', flat=True).distinct()
    statuses = applications.values_list('status', flat=True).distinct()
    
    # Get max funnel count for width calculation
    max_funnel_count = max(funnel_counts) if funnel_counts else 1
    
    context = {
        'funnel_combined': funnel_combined,
        'funnel_labels': funnel_labels,
        'funnel_counts': funnel_counts,
        'max_funnel_count': max_funnel_count,
        'job_performance': job_performance,
        'detailed_report': detailed_report,
        'job_types': job_types,
        'statuses': statuses,
        'status_mapping': status_mapping,
        'total_applications': applications.count(),
        'total_jobs': jobs.count(),
    }
    
    return render(request, 'accounts/recruiter_reports.html', context)