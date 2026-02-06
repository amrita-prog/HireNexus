from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import JobSerializer, JobDetailSerializer, JobPostSerializer, JobApplicationSerializer, MyApplicationSerializer, viewApplicantSerializer, UpdateApplicationStatusSerializer, CountRecruiterJobsSerializer
from rest_framework import status
from jobs.models import Job, Application
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count

# CURL. : CLIENT URL


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_list(request):
    job_res = Job.objects.all() # django objects queryset
    serializer = JobSerializer(job_res, many=True) # many=True for multiple objects
    return Response(serializer.data) # display as JSON response



@api_view(['GET'])
def job_detail(request,id):
    try:
        job= Job.objects.get(id=id)
    except Job.DoesNotExist:
        return Response({"error":"Job not found"},status=status.HTTP_404_NOT_FOUND)
        
    serializer= JobDetailSerializer(job)
    return Response(serializer.data)

@api_view(['POST'])
def create_job_api(request):
    serializer = JobPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message":"Job Created Successfully","job":serializer.data },status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_job_api(request):
    if request.user.roles != 'student':
        return Response({"error": "only students can apply for jobs"},status= status.HTTP_403_FORBIDDEN)
        
    serializer =JobApplicationSerializer(data=request.data)
    
    if serializer.is_valid():
        job = serializer.validated_data['job']
        if Application.objects.filter(job=job,student=request.user).exists():
            return Response({"error":"You have already applied to this job"},status=status.HTTP_400_BAD_REQUEST)
            
        Application.objects.create(job=job,student=request.user)
        return Response({"message": "Job applied successfully"},status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_applications_api(request):
    if request.user.roles != 'student':
        return Response(
            {"error": "only students can view their applications"},
            status= status.HTTP_403_FORBIDDEN
        )
        
    applications = Application.objects.filter(student=request.user)
    serializer = MyApplicationSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_applicants_api(request, job_id):
    if request.user.roles != 'recruiter':
        return Response(
            {"error": "only recruiters can view applicants"},
            status= status.HTTP_403_FORBIDDEN
        )
        
    try:
        job = Job.objects.get(id=job_id, posted_by=request.user)
    except Job.DoesNotExist:
        return Response({"error":"Job not found or you are not authorized to view its applicants"},status=status.HTTP_404_NOT_FOUND)
        
    applications = Application.objects.filter(job=job)
    serializer = viewApplicantSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_application_status_api(request, application_id):
    if request.user.roles != 'recruiter':
        return Response(
            {"error": "only recruiters can update application status"},
            status= status.HTTP_403_FORBIDDEN
        )
    
    try:
        application = Application.objects.select_related('job').get(
            id = application_id,
            job__posted_by = request.user
        )
    except Application.DoesNotExist:
        return Response(
            {"error":"Application not found or not authorized to update its status"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = UpdateApplicationStatusSerializer(application, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message":"Application status updated successfully",
                "status": serializer.data['status']
            }
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def count_recruiter_jobs_api(request):
#     if request.user.roles != 'recruiter':
#         return Response(
#             {"error": "only recruiters can view their job count"},
#             status= status.HTTP_403_FORBIDDEN
#         )
    
    
#     # jobs = (Job.objects.filter(posted_by=request.user).annotate(applicants_counts=Count('application')).order_by('created_at'))

#     jobs = (
#         Job.objects.filter(posted_by=request.user).annotate(applicants_counts=Count('application')).order_by('-created_at')
#     )

#     serializer = CountRecruiterJobsSerializer(jobs, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def count_recruiter_jobs_api(request):
    if request.user.roles !='recruiter':
        return Response(
            {"error":"Only recruiter can view their posted jobs"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    jobs = (
        Job.objects.filter(posted_by=request.user).annotate(applicants_counts=Count('application')).order_by('-created_at')
    )

    serializer = CountRecruiterJobsSerializer(jobs,many=True)
    return Response(serializer.data)