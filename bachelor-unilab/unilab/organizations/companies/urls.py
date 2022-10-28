from django.urls import path

from unilab.organizations.companies.views import (
    CompanyAdminDetail,
    CompanyAdminList,
    CompanyChoices,
    CompanyDetail,
    CompanyList,
    CompanyPicturesDetail,
    CompanyPicturesList,
)

urlpatterns = [
    path(
        "companies",
        CompanyList.as_view(),
        name="company-list",
    ),
    path(
        "companies/<int:pk>",
        CompanyDetail.as_view(),
        name="company-detail",
    ),
    path(
        "companies/choices",
        CompanyChoices.as_view(),
        name="job-choices",
    ),
    path(
        "company-pictures",
        CompanyPicturesList.as_view(),
        name="companypictures-list",
    ),
    path(
        "company-pictures/<int:pk>",
        CompanyPicturesDetail.as_view(),
        name="companypictures-detail",
    ),
    path(
        "company-admins",
        CompanyAdminList.as_view(),
        name="companyadmin-list",
    ),
    path(
        "company-admins/<int:pk>",
        CompanyAdminDetail.as_view(),
        name="companyadmin-detail",
    ),
]
