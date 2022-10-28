from rest_framework import serializers

from unilab.users.models import (
    Certification,
    EducationData,
    ExperienceData,
    ExternalProfile,
    SkillData,
    UniversityCourse,
    UserData,
)


class EducationDataSerializer(serializers.HyperlinkedModelSerializer):
    user_data = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="userdata-detail", many=False
    )

    class Meta:
        model = EducationData
        fields = "__all__"


class ExperienceDataSerializer(serializers.HyperlinkedModelSerializer):
    user_data = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="userdata-detail", many=False
    )

    class Meta:
        model = ExperienceData
        fields = "__all__"


class SkillDataSerializer(serializers.HyperlinkedModelSerializer):
    user_data = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="userdata-detail", many=False
    )

    class Meta:
        model = SkillData
        fields = "__all__"


class ExternalProfileSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="userdata-detail", many=False
    )

    class Meta:
        model = ExternalProfile
        fields = "__all__"


class CertificationSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        view_name="userdata-detail", read_only=True, many=False
    )

    class Meta:
        model = Certification
        fields = "__all__"


class UniversityCourseSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="userdata-detail", many=False
    )

    class Meta:
        model = UniversityCourse
        fields = "__all__"


class UserDataSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="user-detail", many=False
    )
    education_data = EducationDataSerializer(many=True, read_only=True)
    experience_data = ExperienceDataSerializer(many=True, read_only=True)
    external_profiles = ExternalProfileSerializer(many=True, read_only=True)
    university_courses = UniversityCourseSerializer(many=True, read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)
    skill_data = SkillDataSerializer(many=True, read_only=True)

    class Meta:
        model = UserData
        fields = "__all__"
