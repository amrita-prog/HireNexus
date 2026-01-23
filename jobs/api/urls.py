from django.urls import path
from .views import job_list, job_detail, create_job_api

urlpatterns = [
    path('job_listing/', job_list, name='job_listing'),
    path('job_detail/<int:id>/', job_detail, name='job_detail'),
    path('create_job/', create_job_api, name='create_job_api'),
]