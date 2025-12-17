from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.job_create, name='job_create'),
    path('recruiter/jobs/', views.recruiter_job, name='recruiter_jobs'),
    path('edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('student/jobs/', views.view_all_student_jobs, name='all_student_jobs'),
    path('student/job/<int:job_id>/', views.view_job_details, name='view_job_details'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('applicants/<int:job_id>/', views.view_applicants, name='view_applicants'),    
    path('update/application/status/<int:application_id>/', views.update_application_status, name='update_application_status'),
]