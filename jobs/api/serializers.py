from rest_framework import serializers
from jobs.models import Job, Application

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


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Application
        fields= ['job']


class MyApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    company = serializers.CharField(source='job.company', read_only=True)
    
    class Meta:
        model= Application
        fields= ['id','job_title','company','status','applied_at']


class viewApplicantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='student.full_name',read_only=True)
    email = serializers.CharField(source='student.email',read_only=True)
    class Meta:
        model = Application
        fields = ['id','name','email','status','applied_at']


class UpdateApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status']
        

class CountRecruiterJobsSerializer(serializers.Serializer):
    applicants_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Job
        fields = ['id','title','company','location','created_at','salary','deadline','applicants_count']