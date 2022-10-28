from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from unilab.organizations.companies.models import Company


class Job(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    hours_per_week = models.DecimalField(max_digits=3, decimal_places=1)
    salary_per_month = models.PositiveIntegerField()
    publish_date = models.DateField(default=timezone.now)
    requirements = models.TextField(blank=True)
    you_do = models.TextField(blank=True)
    we_offer = models.TextField(blank=True)
    employment_details = models.TextField(blank=True)
    applicants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, through="Application", related_name="job"
    )

    class JobCategories(models.IntegerChoices):
        ADMINISTRATIVE = 1, _("Administrative")
        ARTS_AND_DESIGN = 2, _("Arts & Design")
        BUSINESS = 3, _("Business")
        CONSULTING = 4, _("Consulting")
        CUSTOMER_AND_SUPPORT = 5, _("Customer Services & Support")
        EDUCATION = 6, _("Education")
        ENGINEERING = 7, _("Engineering")
        FINANCE_AND_ACCOUNTING = 8, _("Finance & Accounting")
        HEALTHCARE = 9, _("Healthcare")
        HUMAN_RESOURCES = 10, _("Human Resources")
        IT = 11, _("Information Technology")
        LEGAL = 12, _("Legal")
        MARKETING = 13, _("Marketing")
        MEDIA_AND_COMMUNICATIONS = 14, _("Media & Communications")
        MILITARY_AND_PROTECTIVE = 15, _("Military & Protective Services")
        OPERATIONS = 16, _("Operations")
        OTHER = 17, _("Other")
        PRODUCT_AND_PROJECT_MANAGEMENT = 18, _("Product & Project Management")
        RESEARCH_AND_SCIENCE = 19, _("Research & Science")
        RETAIL_AND_FOOD = 20, _("Retail & Food Services")
        SALES = 21, _("Sales")
        SKILLED_LABOR_AND_MANUFACTURING = 22, _("Skilled Labor & Manufacturing")
        TRANSPORTATION = 23, _("Transportation")

    category = models.IntegerField(choices=JobCategories.choices)

    class JobType(models.IntegerChoices):
        FULL_TIME = 1, _("Full-time")
        PART_TIME = 2, _("Part-time")
        CONTRACT = 3, _("Contract")
        TEMPORARY = 4, _("Temporary")
        INTERNSHIP = 5, _("Internship")

    type = models.IntegerField(choices=JobType.choices)

    def __str__(self):
        return self.title


class Application(models.Model):
    class Meta:
        verbose_name = _("application")
        verbose_name_plural = _("applications")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications"
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    cv = models.FileField(upload_to="cv/%Y/%m/%d/")
    motivation_letter = models.FileField(upload_to="motivation_letter/%Y/%m/%d/")
