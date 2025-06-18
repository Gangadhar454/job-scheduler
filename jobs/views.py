from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job
from .serializers import JobSerializer
from .services import JobScheduler
from django.utils import timezone

class JobListView(APIView):
    def get(self, request):
        """List all jobs"""
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new job"""
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            job = serializer.save(next_run=serializer.validated_data['start_time'])
            scheduler = JobScheduler()
            scheduler.schedule_job(job)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobDetailView(APIView):
    def get(self, request, id):
        """Retrieve job details by ID"""
        try:
            job = Job.objects.get(id=id)
            serializer = JobSerializer(job)
            return Response(serializer.data)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
