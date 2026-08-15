from django.contrib.auth import get_user_model
from rest_framework import serializers

from unilab.organizations.companies.models import Company, CompanyAdmin, CompanyPictures

User = get_user_model()


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="user-detail", many=False
    )
    rating = serializers.ReadOnlyField()
    publish_date = serializers.ReadOnlyField()
    employee_range_verbose = serializers.CharField(
        source="get_employee_range_display", read_only=True
    )
    industry_verbose = serializers.CharField(
        source="get_industry_display", read_only=True
    )

    class Meta:
        model = Company
        # fields = ('url', 'name', 'owner', 'publish_date', 'description', 'video_url', 'website_url', 'rating')
        fields = "__all__"


class CompanyAdminSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name="user-detail", queryset=User.objects.all()
    )
    company = serializers.HyperlinkedRelatedField(
        view_name="company-detail", queryset=Company.objects.all()
    )

    class Meta:
        model = CompanyAdmin
        fields = "__all__"

    def validate(self, data):

        if CompanyAdmin.objects.filter(
            user=data["user"], company=data["company"]
        ).first():
            return serializers.ValidationError("User already an admin")

        return data


class CompanyPicturesSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        view_name="company-detail", many=False, queryset=Company.objects.all()
    )

    class Meta:
        model = CompanyPictures
        fields = "__all__"
