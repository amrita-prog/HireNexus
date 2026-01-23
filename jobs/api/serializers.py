from rest_framework import serializers
from jobs.models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class JobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model= Job
        fields = '__all__'
        
class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model= Job
        fields = ['title','description','company','location','job_type','posted_by','salary','deadline']