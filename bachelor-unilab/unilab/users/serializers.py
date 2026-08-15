from django.contrib.auth import get_user_model
from rest_framework import serializers

from unilab.jobs.models import Application
from unilab.organizations.companies.models import Company, CompanyAdmin
from unilab.organizations.universities.models import UniversityAdmin
from unilab.posts.models import Post
from unilab.users_metadata.models import UserData

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="user-detail")
    companies = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="company-detail",
        queryset=Company.objects.all(),
        required=False,
    )
    applications = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="application-detail",
        queryset=Application.objects.all(),
        required=False,
    )
    password = serializers.CharField(write_only=True)
    user_data = serializers.HyperlinkedRelatedField(
        many=False, view_name="userdata-detail", read_only=True
    )
    # user_type_verbose = serializers.SerializerMethodField()
    voted_posts = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="post-detail",
        queryset=Post.objects.all(),
        required=False,
    )
    occupation = serializers.SerializerMethodField()
    company_admins = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="companyadmin-detail",
        queryset=CompanyAdmin.objects.all(),
        required=False,
    )
    university_admins = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="universityadmin-detail",
        queryset=UniversityAdmin.objects.all(),
        required=False,
    )

    class Meta:
        model = User
        fields = "__all__"

    # hide empty companies attribute for students
    def to_representation(self, instance):
        # if instance.user_type == User.UserType.STUDENT:
        #     del ret['companies']

        return super().to_representation(instance)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        UserData.objects.create(user=user)

        return user

    def get_occupation(self, obj):
        return obj.user_data.occupation


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
