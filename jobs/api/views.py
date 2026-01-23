from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import JobSerializer, JobDetailSerializer, JobPostSerializer
from rest_framework import status
from jobs.models import Job
from rest_framework.permissions import IsAuthenticated

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