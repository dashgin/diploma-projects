from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from unilab.organizations.models import OrganizationPage


class Company(OrganizationPage):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="companies",
        on_delete=models.CASCADE,
    )
    admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        through="CompanyAdmin",
    )
    image = models.ImageField(
        upload_to="company_image/%Y/%m/%D/",
        default="defaults/company.jpg",
    )

    class EmployeeRange(models.IntegerChoices):
        TINY = (1, _("1-20 employees"))
        SMALL = (2, _("21-100 employees"))
        MEDIUM = (3, _("101-200 employees"))
        LARGE = (4, _("201-500 employees"))
        HUGE = 5, _("501+ employees")

    employee_range = models.IntegerField(choices=EmployeeRange.choices)

    class Industries(models.IntegerChoices):
        ENERGY = (1, _("Energy, Utilities and Resources"))
        GOVERNMENT = (2, _("Government and Public Sector"))
        PHARMA = (3, _("Pharmaceuticals and Life Sciences"))
        ESTATE = (4, _("Real Estate"))
        SPORTS = (5, _("Sports Business Advisory"))
        FINANCE = (6, _("Financial Services"))
        HEALTH = (7, _("Health Services"))
        MANUFACTURE = (8, _("Industrial Manufacturing"))
        RETAIL = (9, _("Retail and Consumer Goods"))
        TECH = 10, _("Technology, Media, and Telecommunications")
        OTHER = 11, _("Other")

    industry = models.IntegerField(choices=Industries.choices)

    class Meta:
        verbose_name = _("company")
        verbose_name_plural = _("companies")


class CompanyPictures(models.Model):
    class Meta:
        verbose_name = _("company picture")
        verbose_name_plural = _("company pictures")

    owner = models.ForeignKey(
        Company, related_name="pictures", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="company_pictures/%Y/%m/%D/")
    description = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)


class CompanyAdmin(models.Model):
    class Meta:
        verbose_name = _("company Admin")
        verbose_name_plural = _("company Admins")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_admin",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
    )

    post_permission = models.BooleanField(default=False)
    comment_permission = models.BooleanField(default=False)
    edit_profile_permission = models.BooleanField(default=False)
    accept_applicants_permission = models.BooleanField(default=False)

    create_jobs_permission = models.BooleanField(default=False)
    view_applicants_permission = models.BooleanField(default=False)
    edit_admins_permission = models.BooleanField(default=False)
