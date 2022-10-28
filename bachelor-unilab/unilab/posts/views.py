from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response

from unilab.organizations.companies.models import Company
from unilab.posts.models import Comment, FeedbackForm, Post, PostReport, Vote
from unilab.posts.serializers import (
    CommentSerializer,
    FeedbackFormSerializer,
    PostReportSerializer,
    PostSerializer,
    VoteSerializer,
)
from unilab.utils.permissions import IsOwner

User = get_user_model()


class FeedbackFormDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeedbackForm.objects.all()
    serializer_class = FeedbackFormSerializer


class FeedbackFormList(generics.ListCreateAPIView):
    queryset = FeedbackForm.objects.all()
    serializer_class = FeedbackFormSerializer


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if company_url := self.request.query_params.get("company"):
            company = Company.objects.filter(pk=url_to_pk(company_url)).first()
            serializer.save(company=company, owner=user)

        else:
            serializer.save(owner=user)

    def get_queryset(self):
        queryset = Comment.objects.all()
        email = self.request.query_params.get("email")
        company_owner = self.request.query_params.get("company_owner")

        if email is not None:
            user = User.objects.filter(email=email).first()
            queryset = queryset.filter(owner=user)

        elif company_owner is not None:
            company_obj = Company.objects.filter(pk=url_to_pk(company_owner)).first()
            queryset = queryset.filter(company=company_obj)

        return queryset


class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class VoteList(generics.ListCreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if company_url := self.request.query_params.get("company"):
            company = Company.objects.filter(pk=url_to_pk(company_url)).first()
            serializer.save(company=company, user=user)

        else:
            serializer.save(user=user)

    def delete(self, request, *args, **kwargs):
        company_url = self.request.query_params.get("company")
        post_url = request.POST["post"]
        post_pk = url_to_pk(post_url)
        post = Post.objects.filter(pk=post_pk).first()
        user = self.request.user

        if company_url is not None:  # if an employer user votes
            assert (
                user.user_type == user.UserType.EMPLOYER
            ), "Only employer users can give a company as vote owner"
            company = Company.objects.filter(pk=url_to_pk(company_url))
            Vote.objects.filter(company=company, post=post).delete()

        else:  # if a student votes

            Vote.objects.filter(user=user, post=post).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_filters = ["id, publish_date, score"]
    ordering = ["-id"]

    def perform_create(self, serializer):
        user = self.request.user
        if company_url := self.request.query_params.get("company"):
            company = Company.objects.filter(pk=url_to_pk(company_url)).first()
            serializer.save(company=company, owner=user)

        else:
            serializer.save(owner=user)

    def get_queryset(self):
        queryset = Post.objects.all()
        email = self.request.query_params.get("email")
        company_owner = self.request.query_params.get("company_owner")
        if email is not None:
            user = User.objects.filter(email=email).first()
            queryset = queryset.filter(owner=user)

        elif company_owner is not None:
            company_obj = Company.objects.filter(pk=url_to_pk(company_owner)).first()
            queryset = queryset.filter(company=company_obj)

        return queryset


class PostReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostReport.objects.all()
    serializer_class = PostReportSerializer


class PostReportList(generics.ListCreateAPIView):
    queryset = PostReport.objects.all()
    serializer_class = PostReportSerializer
