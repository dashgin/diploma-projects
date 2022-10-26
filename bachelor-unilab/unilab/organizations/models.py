from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class OrganizationPage(models.Model):
    """
    Base for university, company and other type organizations
    """

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(blank=True, null=True)
    video_url = models.CharField(max_length=200, blank=True)
    website_url = models.CharField(max_length=200, blank=True)
    publish_date = models.DateField(default=timezone.now)
    country = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
