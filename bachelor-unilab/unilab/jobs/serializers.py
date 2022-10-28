from rest_framework import serializers

from unilab.jobs.models import Application, Job
from unilab.organizations.companies.models import Company
from unilab.organizations.companies.serializers import CompanySerializer


class JobSerializer(serializers.HyperlinkedModelSerializer):
    publish_date = serializers.ReadOnlyField()
    owner = serializers.HyperlinkedRelatedField(
        view_name="company-detail",
        queryset=Company.objects.all(),
        write_only=True,
        required=True,
    )
    company = serializers.SerializerMethodField()
    category_verbose = serializers.CharField(
        source="get_category_display", read_only=True
    )
    type_verbose = serializers.CharField(source="get_type_display", read_only=True)
    applications = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="application-detail",
        queryset=Application.objects.all(),
        required=False,
    )

    class Meta:
        model = Job
        fields = "__all__"

    def get_company(self, job):
        # sourcery skip: inline-immediately-returned-variable
        return CompanySerializer(
            job.owner, context={"request": self.context["request"]}
        ).data


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    job = JobSerializer(read_only=True, many=False)

    # job = serializers.HyperlinkedRelatedField(view_name='job-detail', queryset=Job.objects.all())

    class Meta:
        model = Application
        fields = "__all__"

    def create(self, validated_data):
        # delete previous application from the same user on same job
        user = validated_data["user"]
        job = validated_data["job"]

        previous_vote = Application.objects.filter(user=user, job=job)
        previous_vote.delete()

        return super().create(validated_data)
