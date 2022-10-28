from django.urls import path

from unilab.organizations.universities.views import (
    UniversityAdminDetail,
    UniversityAdminList,
    UniversityDetail,
    UniversityList,
)

urlpatterns = [
    path(
        "university-admins",
        UniversityAdminList.as_view(),
        name="universityadmin-list",
    ),
    path(
        "university-admins/<int:pk>",
        UniversityAdminDetail.as_view(),
        name="universityadmin-detail",
    ),
    path(
        "universities",
        UniversityList.as_view(),
        name="university-list",
    ),
    path(
        "universities/<int:pk>",
        UniversityDetail.as_view(),
        name="university-detail",
    ),
]
