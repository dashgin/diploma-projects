import re

from django.contrib.auth import get_user_model
from rest_framework import filters, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from unilab.organizations.companies.models import Company, CompanyAdmin, CompanyPictures
from unilab.organizations.companies.serializers import (
    CompanyAdminSerializer,
    CompanyPicturesSerializer,
    CompanySerializer,
)
from unilab.utils.data_converters import url_to_pk
from unilab.utils.permissions import IsCompanyOrReadOnly, IsOwner

User = get_user_model()


class CompanyAdminList(generics.ListCreateAPIView):
    queryset = CompanyAdmin.objects.all()
    serializer_class = CompanyAdminSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        if user_url := self.request.query_params.get("user"):
            user_pk = url_to_pk(user_url)
            admin = CompanyAdmin.objects.filter(user=user_pk).first()
            admin.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("user_url parameter needed")

    def get_queryset(self):
        user = self.request.query_params.get("user")
        company = self.request.query_params.get("company")
        if user is None and company is None:
            return self.queryset

        if user is not None and company is None:
            user_pk = re.search(r"users/(\d+)", user)[1]
            return CompanyAdmin.objects.filter(user=user_pk)

        if user is None and company is not None:
            company_pk = re.search(r"companies/(\d+)", company)[1]
            return CompanyAdmin.objects.filter(company=company_pk)

        if user is not None and company is not None:
            user_pk = re.search(r"users/(\d+)", user)[1]
            company_pk = re.search(r"companies/(\d+)", company)[1]
            return CompanyAdmin.objects.filter(company=company_pk, user=user_pk)


class CompanyAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyAdmin.objects.all()
    serializer_class = CompanyAdminSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user == instance.company.owner:
            raise ValidationError("Owner cannot be removed as admin")


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsCompanyOrReadOnly, IsOwner]


class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsCompanyOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    ordering = ["-id"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        admin = CompanyAdminSerializer(
            data={
                "user": serializer.data["owner"],
                "company": serializer.data["url"],
                "post_permission": "True",
                "comment_permission": "True",
                "create_jobs_permission": "True",
                "accept_applicants_permission": "True",
                "view_applicants_permission": "True",
                "edit_profile_permission": "True",
            }
        )
        admin.is_valid()
        admin.save()

    def get_queryset(self):
        queryset = Company.objects.all()
        email = self.request.query_params.get("email")
        if email is not None:
            user = User.objects.filter(email=email).first()
            queryset = queryset.filter(owner=user)

        return queryset


class CompanyChoices(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "industry_choices": Company.Industries.choices,
                "employee_choices": Company.EmployeeRange.choices,
            }
        )


class CompanyPicturesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyPictures.objects.all()
    serializer_class = CompanyPicturesSerializer
    # permission_classes = [IsCompanyOrReadOnly, IsOwner]


class CompanyPicturesList(generics.ListCreateAPIView):
    queryset = CompanyPictures.objects.all()
    serializer_class = CompanyPicturesSerializer

    # permission_classes = []

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.company)

    def get_queryset(self):
        queryset = CompanyPictures.objects.all()
        owner = self.request.query_params.get("owner")
        if owner is not None:
            pk = url_to_pk(owner)
            company = Company.objects.filter(pk=pk).first()
            queryset = queryset.filter(owner=company)
        return queryset
