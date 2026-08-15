from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

from unilab.jobs.models import Job
from unilab.organizations.companies.models import Company
from unilab.organizations.universities.models import University
from unilab.posts.models import Comment, Post
from unilab.users_metadata.models import EducationData, ExperienceData, UserData
from unilab.utils.data_converters import url_to_pk

User = get_user_model()


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners and super-admins of an object to edit it.
    """

    # makes POST requests valid for unauthenticated users

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True

        if isinstance(obj, User):
            return obj == request.user
        # TODO: Test UserData, EducationData, ExperienceData
        if isinstance(obj, UserData):
            return obj.user == request.user
        if isinstance(obj, EducationData):
            return obj.user_data.user == request.user
        if isinstance(obj, ExperienceData):
            return obj.user_data.user == request.user
        if isinstance(obj, Job):
            return obj.owner in request.user.companies.all()
        if isinstance(obj, Company):
            return obj.owner == request.user
        if isinstance(obj, Post):
            return obj.owner == request.user
        if isinstance(obj, Comment):
            return obj.owner == request.user


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True

        if isinstance(obj, University):
            return request.user in obj.admins.all()

        if isinstance(obj, Company):
            return request.user in obj.admins.all()


class UserViewPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "PATCH" or list(request.POST) != ["university"]:
            return True
        if request.POST.get("university"):
            uni_pk = url_to_pk(request.POST.get("university"))
            uni = University.objects.filter(pk=uni_pk).first()
            return request.user in uni.admins.all()
        else:
            # if trying to set university to null then check on individual object
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS or request.method == "POST":
            return True

        if request.method == "PATCH" and list(request.POST) == ["university"]:
            # only university of student is allowed to delete him from their uni
            if request.POST["university"] == "":
                return obj.university in request.user.university_admin.all()

            else:
                return True

        elif request.method == "PATCH" and (
            "allowed_company_creation" in list(request.POST)
            or "allowed_university_creation" in list(request.POST)
        ):
            return request.user.is_superuser

        else:
            return request.user == obj


class UniversityViewPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method not in permissions.SAFE_METHODS and request.method == "POST":
            return request.user.allowed_university_creation
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS or request.method == "POST":
            return True

        else:
            return obj in request.user.university_admin


class IsCompanyOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow companies and super-admins to create jobs, but not students. All users can GET.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        else:
            return bool(
                not isinstance(request.user, AnonymousUser)
                and request.user.allowed_company_creation
            )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated


class CompanyOwner(permissions.BasePermission):
    """ "Check that the company creating the job is owned by the user"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        elif request.user.is_anonymous:
            return False

        else:
            if owner_url := request.POST.get("owner"):
                owner = Company.objects.filter(pk=url_to_pk(owner_url)).first()
            else:
                self.message = "Please add the company owner url"
                return False
            return owner in request.user.companies.all()
