from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from unilab.organizations.models import OrganizationPage


class University(OrganizationPage):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="universities",
        on_delete=models.CASCADE,
    )
    admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        through="UniversityAdmin",
        related_name="university_admin_set",
    )
    image = models.ImageField(
        upload_to="company_image/%Y/%m/%D/",
        default="defaults/university.jpg",
    )

    class StudentRange(models.IntegerChoices):
        SMALL = (
            1,
            _("<5000 students"),
        )
        MEDIUM = (
            2,
            _("5000-15000 students"),
        )
        LARGE = (
            3,
            _(">15000 students"),
        )

    student_range = models.IntegerField(
        choices=StudentRange.choices, blank=True, null=True
    )

    class Meta:
        verbose_name = _("university")
        verbose_name_plural = _("universities")


class UniversityAdmin(models.Model):
    class Meta:
        verbose_name = _("university admin")
        verbose_name_plural = _("university admins")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="university_admin",
    )
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    post_permission = models.BooleanField(default=False)
    comment_permission = models.BooleanField(default=False)
    edit_profile_permission = models.BooleanField(default=False)
    accept_student_application_permission = models.BooleanField(default=False)
