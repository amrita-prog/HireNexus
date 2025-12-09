from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobPostForm
from .models import Job, JOB_TYPE_CHOICES, Application
from django.contrib import messages

# Create your views here.

@login_required
def job_create(request):
    if not request.user.roles == 'recruiter':
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        print(request.user)
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request,'Job Posted Successfully')
            return redirect('recruiter_dashboard')
        else:
            print("FORM ERRORS:", form.errors)
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobPostForm()
    
    return render(request,'jobs/jobs_create.html',{'form_data':form})

@login_required
def recruiter_job(request):
    if not request.user.roles == 'recruiter':
        return redirect('student_dashboard')
    
    myjobs = Job.objects.filter(posted_by = request.user).order_by('-created_at') # "-" for descending order
    return render(request,'jobs/recruiter_jobs.html',{'jobs':myjobs})


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user) #table pass if exist

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job) # instance to populate form with existing data
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully.')
            return redirect('recruiter_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobPostForm(instance=job)
    return render(request, 'jobs/edit_job.html', {'form_data': form})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully.')
        return redirect('recruiter_dashboard')
    return render(request, 'jobs/recruiter_jobs.html', {'jobs': job})


def view_all_student_jobs(request):
    all_jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'jobs/all_student_jobs.html', {'job_data': all_jobs})
    
@login_required
def view_job_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})


def apply_job(request, job_id):
    if not request.user.roles == 'student' or not request.user.is_authenticated:
        messages.error(request, "Only students can apply for jobs.")
        return redirect('login')
    job = get_object_or_404(Job, id=job_id)
    already_applied = Application.objects.filter(job=job, student=request.user).exists()
    if already_applied:
        messages.warning(request, "You have already applied for this job.")
    else:
        Application.objects.create(job=job, student=request.user)
        messages.success(request, "Your application has been submitted.")

    return redirect('all_student_jobs')