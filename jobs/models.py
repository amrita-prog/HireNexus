from django.db import models
from django.conf import settings # for customUser in accounts app

# Create your models here.
JOB_TYPE_CHOICES = [
    ('FULL_TIME', 'Full Time'),
    ('PART_TIME', 'Part Time'),
    ('INTERNSHIP', 'Internship'),
    ('CONTRACT', 'Contract'),
]

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    salary = models.IntegerField()
    deadline = models.DateField()

    def __str__(self):
        return f"{self.title} at {self.company}"
    

APPLICATION_STATUS_CHOICES = [
    ('applied', 'Applied'),
    ('shortlisted', 'Shortlisted'),
    ('intervie_1', 'L1 Cleared '),
    ('interview_technical', 'Technical Cleared'),
    ('hr_cleared', 'HR Cleared'),
    ('rejected', 'Rejected'),
    ('offered', 'Offered'),
    ('hold_on', 'Hold On'),
]

class Application(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE) #relation to Job model
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=APPLICATION_STATUS_CHOICES, default='applied')
    status_notified = models.BooleanField(default=False)

    class Meta:
        unique_together = ('job', 'student') # to prevent multiple applications for the same job by the same student

    def __str__(self):
        return f"{self.student.username} applied for {self.job.title}"