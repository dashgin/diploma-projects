from rest_framework import filters, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from unilab.jobs.models import Application, Job
from unilab.jobs.serializers import ApplicationSerializer, JobSerializer
from unilab.organizations.companies.models import Company
from unilab.utils.permissions import IsAdmin, IsOwner, IsCompanyOrReadOnly


class ApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class ApplicationList(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def perform_create(self, serializer):
        user = self.request.user
        job_url = self.request.POST["job"]
        job = Job.objects.filter(pk=url_to_pk(job_url)).first()
        serializer.save(user=user, job=job)

    def get_queryset(self):
        user = self.request.query_params.get("user")
        return (
            Application.objects.filter(user=url_to_pk(user))
            if user
            else Application.objects.all()
        )


class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsCompanyOrReadOnly, IsOwner]


class JobList(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Job.objects.all()
        owner = self.request.query_params.get("owner")
        if owner is not None:
            pk = url_to_pk(owner)
            company = Company.objects.filter(pk=pk).first()
            queryset = queryset.filter(owner=company)
        return queryset


class JobChoices(APIView):
    def get(self, request):
        data = {
            "category_choices": Job.JobCategories.choices,
            "type_choices": Job.JobType.choices,
        }
        return Response(data)
