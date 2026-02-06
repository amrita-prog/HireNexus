from django.urls import path
from .views import job_list, job_detail, create_job_api, apply_job_api, my_applications_api, view_applicants_api, update_application_status_api, count_recruiter_jobs_api

urlpatterns = [
    path('job_listing/', job_list, name='job_listing'),
    path('job_detail/<int:id>/', job_detail, name='job_detail'),
    path('create_job/', create_job_api, name='create_job_api'),
    path('apply_job/',apply_job_api,name="apply_job"),
    path('my_applications/',my_applications_api,name="my_applications_api"),
    path('view_applicants/<int:job_id>/', view_applicants_api, name='view_applicants_api'),
    path('update_application_status/<int:application_id>/', update_application_status_api, name='update_application_status_api'),
    path('count_recruiter_jobs/', count_recruiter_jobs_api, name='count_recruiter_jobs_api'),
]