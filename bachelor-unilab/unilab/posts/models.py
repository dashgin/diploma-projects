from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from unilab.organizations.companies.models import Company


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(
        upload_to="post_images/%Y/%m/%D/",
        blank=True,
        null=True,
    )
    publish_date = models.DateField(default=timezone.now)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="posts",
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(
        Company,
        blank=True,
        on_delete=models.CASCADE,
        null=True,
    )


class Vote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class VoteTypes(models.IntegerChoices):
        UPVOTE = 1, _("Upvote")
        DOWNVOTE = 2, _("Downvote")

    v_type = models.PositiveSmallIntegerField(choices=VoteTypes.choices)


class Comment(models.Model):

    content = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    post = models.ForeignKey(
        Post,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    publish_date = models.DateField(default=timezone.now)


class PostReport(models.Model):

    post = models.ForeignKey(
        Post,
        related_name="reports",
        on_delete=models.CASCADE,
    )
    description = models.TextField()

    class Reasons(models.IntegerChoices):
        SPAM = 1, _("Spam")
        OFFENSIVE = 2, _("Offensive")
        MISLEADING = 3, _("Misleading")

    reason = models.PositiveSmallIntegerField(choices=Reasons.choices)


class FeedbackForm(models.Model):
    class Meta:
        verbose_name = "feedback form"
        verbose_name_plural = "feedback forms"

    class Scale(models.IntegerChoices):
        VERY_BAD = 1, "Very Bad"
        BAD = 2, "Bad"
        COULD_BE_BETTER = 3, "Could be Better"
        ALRIGHT = 4, "Alright"
        GOOD = 5, "Good"
        VERY_GOOD = 6, "Very Good"
        INCREDIBLE = 7, "Incredible"

    institution = models.TextField()
    country = models.TextField()
    looks = models.PositiveSmallIntegerField(choices=Scale.choices)
    accessibility = models.PositiveSmallIntegerField(choices=Scale.choices)
    usability = models.PositiveSmallIntegerField(choices=Scale.choices)
    future_use = models.BooleanField()
    recommend = models.BooleanField()
    comments = models.TextField()
