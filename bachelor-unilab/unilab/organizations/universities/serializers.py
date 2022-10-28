from django.contrib.auth import get_user_model
from rest_framework import serializers

from unilab.organizations.universities.models import University, UniversityAdmin

User = get_user_model()


class UniversitySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="user-detail", many=False
    )
    rating = serializers.ReadOnlyField()
    student_range_verbose = serializers.CharField(
        source="get_student_range_display", read_only=True, allow_blank=True
    )
    students = serializers.HyperlinkedRelatedField(
        many=True, queryset=User.objects.all(), view_name="user-detail", required=False
    )

    class Meta:
        model = University
        fields = "__all__"


class UniversityAdminSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name="user-detail", queryset=User.objects.all()
    )
    university = serializers.HyperlinkedRelatedField(
        view_name="university-detail", queryset=University.objects.all()
    )

    class Meta:
        model = UniversityAdmin
        fields = "__all__"

    def validate(self, data):
        # check for duplicates
        user = data["user"]
        university = data["university"]

        if existing := UniversityAdmin.objects.filter(
            user=user, university=university
        ).first():
            return serializers.ValidationError("User already an admin")

        return data
