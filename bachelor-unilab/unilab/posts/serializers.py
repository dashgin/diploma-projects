from django.contrib.auth import get_user_model
from rest_framework import serializers

from unilab.organizations.companies.models import Company
from unilab.organizations.companies.serializers import CompanySerializer
from unilab.posts.models import Comment, FeedbackForm, Post, PostReport, Vote
from unilab.utils.data_converters import url_to_pk

User = get_user_model()


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    publish_date = serializers.ReadOnlyField()
    owner = UserSerializer(read_only=True, many=False)
    company = CompanySerializer(read_only=True, many=False)
    post = serializers.HyperlinkedRelatedField(
        view_name="post-detail", many=False, queryset=Post.objects.all()
    )

    class Meta:
        model = Comment
        fields = "__all__"


class PostSerializer(serializers.HyperlinkedModelSerializer):
    publish_date = serializers.ReadOnlyField()
    owner = UserSerializer(read_only=True, many=False)
    company = CompanySerializer(read_only=True, many=False, required=False)
    comments = CommentSerializer(many=True, read_only=True)
    votes = serializers.SerializerMethodField(method_name="create_votes")
    score = serializers.SerializerMethodField(method_name="create_score")
    user_vote = serializers.SerializerMethodField(method_name="create_user_vote")

    class Meta:
        model = Post
        fields = "__all__"

    def create_score(self, post):
        upvotes = Vote.objects.filter(post=post, type=1)
        downvotes = Vote.objects.filter(post=post, type=2)
        return len(upvotes) - len(downvotes)

    def create_votes(self, post):
        votes = Vote.objects.filter(post=post)
        serializer = VoteSerializer(
            many=True,
            data=list(votes),
            context={"request": self.context.get("request")},
        )
        serializer.is_valid()
        serialized_votes = serializer.data
        output = {"upvotes": [], "downvotes": []}
        for vote in serialized_votes:
            if vote["type"] == 1:
                output["upvotes"] += [vote["user"]]
            else:
                output["downvotes"] += [vote["user"]]

        return output

    def create_user_vote(self, post):
        # show what the user requesting the api voted
        user = self.context["request"].user
        if company_url := self.context["request"].query_params.get("company"):
            company_url = self.context["request"].query_params.get("company")
            assert (
                company_url is not None
            ), "Employer user should always specify a company in query (?company=url)"
            company_pk = url_to_pk(company_url)
            company = Company.objects.filter(pk=company_pk).first()
            vote = Vote.objects.filter(post=post, company=company).first()
        else:
            vote = Vote.objects.filter(post=post, user=user).first()

        vote_label = None
        if vote:
            # go through all types of labels and get the one matching the attribute type of vote (int).
            for label_tup in vote.TYPE_CHOICES:
                if label_tup[0] == vote.type_:
                    vote_label = label_tup[1]
                    break

        return vote_label


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name="user-detail", queryset=User.objects.all()
    )
    company = serializers.HyperlinkedRelatedField(
        view_name="company-detail", queryset=Company.objects.all(), required=False
    )
    # user_data = serializers.HyperlinkedRelatedField(view_name='userdata-detail', queryset=UserData.objects.all())
    post = serializers.HyperlinkedRelatedField(
        view_name="post-detail", queryset=Post.objects.all()
    )

    class Meta:
        model = Vote
        fields = "__all__"

    def create(self, validated_data):
        # delete previous votes from the same user on same post
        user = validated_data["user"]
        post = validated_data["post"]
        company = validated_data.get("company")
        if company is not None:
            assert (
                user.user_type == user.UserType.EMPLOYER
            ), "Only employer users can give a company as vote owner (custom code)"
            previous_vote = Vote.objects.filter(company=company, post=post)
        else:
            previous_vote = Vote.objects.filter(user=user, post=post)
        previous_vote.delete()

        return super().create(validated_data)


class PostReportSerializer(serializers.HyperlinkedModelSerializer):
    post = serializers.HyperlinkedRelatedField(
        view_name="post-detail", queryset=Post.objects.all()
    )

    class Meta:
        model = PostReport
        fields = "__all__"


class FeedbackFormSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FeedbackForm
        fields = "__all__"
