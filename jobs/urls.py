from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.job_create, name='job_create'),
    path('recruiter/jobs/', views.recruiter_job, name='recruiter_jobs'),
    path('edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
]