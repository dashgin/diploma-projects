from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserData(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="user_data",
        on_delete=models.CASCADE,
    )
    occupation = models.CharField(
        blank=True,
        max_length=100,
        default="Student",
    )
    biography = models.CharField(blank=True, max_length=100)
    location = models.CharField(blank=True, max_length=100)
    website = models.TextField(blank=True)

    class Meta:
        verbose_name = _("User Data")
        verbose_name_plural = _("Users Data")


class ExternalProfile(models.Model):

    owner = models.ForeignKey(
        UserData,
        related_name="external_profiles",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)


class SkillData(models.Model):

    user_data = models.ForeignKey(
        UserData,
        related_name="skill_data",
        on_delete=models.CASCADE,
    )
    category = models.CharField(max_length=200)
    skill = models.CharField(max_length=200)

    class Meta:
        verbose_name = _("Skill Data")
        verbose_name_plural = verbose_name


class Certification(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(
        UserData,
        related_name="certifications",
        on_delete=models.CASCADE,
    )
    description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    proof = models.ImageField(
        upload_to="certification_proof/%Y/%m/%D/",
        null=True,
        blank=True,
    )


class UniversityCourse(models.Model):
    owner = models.ForeignKey(
        UserData,
        related_name="university_courses",
        on_delete=models.CASCADE,
    )
    course = models.CharField(max_length=200)
    ects = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    description = models.CharField(max_length=200)


class EducationData(models.Model):
    user_data = models.ForeignKey(
        UserData,
        related_name="education_data",
        on_delete=models.CASCADE,
    )
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(
        upload_to="education_image/%Y/%m/%D/",
        default="defaults/university.jpg",
    )

    class Meta:
        verbose_name = _("education data")
        verbose_name_plural = _("education data")


class ExperienceData(models.Model):
    class Meta:
        verbose_name = _("experience data")
        verbose_name_plural = _("experience data")

    user_data = models.ForeignKey(
        "UserData", related_name="experience_data", on_delete=models.CASCADE
    )
    company = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(
        upload_to="experience_image/%Y/%m/%D/", default="defaults/experience.jpg"
    )
