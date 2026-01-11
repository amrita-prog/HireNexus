from django.urls import path
from . import views

urlpatterns = [
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('recruiter/dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('recruiter/applications/', views.recruiter_applications, name='recruiter_applications'),
    path('recruiter/reports/', views.recruiter_reports, name='recruiter_reports'),
    path('signup/student/', views.student_signup, name='student_signup'),
    path('signup/recruiter/', views.recruiter_signup, name='recruiter_signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('applied/jobs/',views.student_applied_jobs, name='student_applied_jobs'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]