from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from unilab.organizations.universities.models import University, UniversityAdmin
from unilab.organizations.universities.serializers import (
    UniversityAdminSerializer,
    UniversitySerializer,
)


class UniversityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [UniversityViewPermissions]


class UniversityList(generics.ListCreateAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [UniversityViewPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    ordering = ["-id"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        admin = UniversityAdminSerializer(
            data={
                "user": serializer.data["owner"],
                "university": serializer.data["url"],
            }
        )
        admin.is_valid()
        admin.save()

    def get_queryset(self):
        queryset = University.objects.all()
        email = self.request.query_params.get("email")
        if email is not None:
            user = User.objects.filter(email=email).first()
            queryset = queryset.filter(owner=user)

        return queryset


class UniversityAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UniversityAdmin.objects.all()
    serializer_class = UniversityAdminSerializer
    permission_classes = [IsAuthenticated]


class UniversityAdminList(generics.ListCreateAPIView):
    queryset = UniversityAdmin.objects.all()
    serializer_class = UniversityAdminSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        if user_url := self.request.query_params.get("user"):
            user_pk = url_to_pk(user_url)
            admin = UniversityAdmin.objects.filter(user=user_pk).first()
            admin.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("user_url parameter needed")

    def get_queryset(self):
        user = self.request.query_params.get("user")
        university = self.request.query_params.get("university")
        if user is None and university is None:
            return self.queryset

        if user is not None and university is None:
            user_pk = re.search(r"users/(\d+)", user)[1]
            return UniversityAdmin.objects.filter(user=user_pk)

        if user is None and university is not None:
            university_pk = re.search(r"companies/(\d+)", university)[1]
            return UniversityAdmin.objects.filter(company=university_pk)

        if user is not None and university is not None:
            user_pk = re.search(r"users/(\d+)", user)[1]
            university_pk = re.search(r"companies/(\d+)", university)[1]
            return UniversityAdmin.objects.filter(company=university_pk, user=user_pk)
