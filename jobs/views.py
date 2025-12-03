from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobPostForm
from .models import Job, JOB_TYPE_CHOICES
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