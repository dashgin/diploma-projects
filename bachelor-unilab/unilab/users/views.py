import re

import django_filters.rest_framework
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from unilab.organizations.universities.models import University
from unilab.users.serializers import ChangePasswordSerializer, UserSerializer
from unilab.utils.permissions import UserViewPermissions

User = get_user_model()


class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserViewPermissions]


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserViewPermissions]
    filter_backends = [
        filters.SearchFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    ]
    filterset_fields = ["allowed_company_creation", "allowed_university_creation"]
    search_fields = ["first_name", "last_name", "email"]

    def get_queryset(self):
        if not_admin_of := self.request.query_params.get("not_admin_of"):
            if "companies" in not_admin_of:
                pk = re.search(r"companies/(\d+)", not_admin_of)[1]
                admin_list = Company.objects.filter(pk=pk).first().admins.all()
                admins_pks = [user.id for user in admin_list]
                return User.objects.exclude(pk__in=admins_pks)

            elif "universities" in not_admin_of:
                pk = re.search(r"universities/(\d+)", not_admin_of)[1]
                admin_list = University.objects.filter(pk=pk).first().admins.all()
                admins_pks = [user.id for user in admin_list]
                return User.objects.exclude(pk__in=admins_pks)

        if not_student_of := self.request.query_params.get("not_student_of"):
            pk = re.search(r"universities/(\d+)", not_student_of)[1]
            student_list = University.objects.filter(pk=pk).first().students.all()
            student_pks = [user.id for user in student_list]
            return User.objects.exclude(pk__in=student_pks)

        else:
            return User.objects.all()
