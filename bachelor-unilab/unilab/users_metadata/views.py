import re

from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from unilab.users_metadata.models import (
    Certification,
    EducationData,
    ExperienceData,
    ExternalProfile,
    SkillData,
    UniversityCourse,
    UserData,
)
from unilab.users_metadata.serializers import (
    CertificationSerializer,
    EducationDataSerializer,
    ExperienceDataSerializer,
    ExternalProfileSerializer,
    SkillDataSerializer,
    UniversityCourseSerializer,
    UserDataSerializer,
)
from unilab.utils.permissions import IsOwner

User = get_user_model()


User = get_user_model()


class EducationDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EducationData.objects.all()
    serializer_class = EducationDataSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class EducationDataList(generics.ListCreateAPIView):
    queryset = EducationData.objects.all()
    serializer_class = EducationDataSerializer

    def perform_create(self, serializer):
        serializer.save(user_data=self.request.user.user_data)


class ExperienceDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExperienceData.objects.all()
    serializer_class = ExperienceDataSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class ExperienceDataList(generics.ListCreateAPIView):
    queryset = ExperienceData.objects.all()
    serializer_class = ExperienceDataSerializer

    def perform_create(self, serializer):
        serializer.save(user_data=self.request.user.user_data)


class SkillDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SkillData.objects.all()
    serializer_class = ExperienceDataSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class SkillDataList(generics.ListCreateAPIView):
    queryset = SkillData.objects.all()
    serializer_class = SkillDataSerializer

    def perform_create(self, serializer):
        serializer.save(user_data=self.request.user.user_data)


class UserDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class UserDataList(generics.ListCreateAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.query_params.get("user")
        if user is None:
            return UserData.objects.filter(user=self.request.user.id)
        pk = re.search(r"users/(\d+)", user)[1]
        return UserData.objects.filter(user=pk)


class ExternalProfileList(generics.ListCreateAPIView):
    queryset = ExternalProfile.objects.all()
    serializer_class = ExternalProfileSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.user_data)


class ExternalProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExternalProfile.objects.all()
    serializer_class = ExternalProfileSerializer


class UniversityCourseList(generics.ListCreateAPIView):
    queryset = UniversityCourse.objects.all()
    serializer_class = UniversityCourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.user_data)


class UniversityCourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UniversityCourse.objects.all()
    serializer_class = UniversityCourseSerializer


class CertificationList(generics.ListCreateAPIView):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.user_data)


class CertificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
