from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import JobSerializer
from jobs.models import Job


@api_view(['GET'])
def job_list(request):
    job_res = Job.objects.all() # django objects queryset
    serializer = JobSerializer(job_res, many=True) # many=True for multiple objects
    return Response(serializer.data) # display as JSON response


# CURL. : CLIENT URL