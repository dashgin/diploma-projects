from django.urls import path

from unilab.jobs.views import (
    ApplicationDetail,
    ApplicationList,
    JobChoices,
    JobDetail,
    JobList,
)

urlpatterns = [
    path(
        "jobs",
        JobList.as_view(),
        name="job-list",
    ),
    path(
        "jobs/<int:pk>",
        JobDetail.as_view(),
        name="job-detail",
    ),
    path(
        "jobs/choices",
        JobChoices.as_view(),
        name="job-choices",
    ),
    path(
        "applications",
        ApplicationList.as_view(),
        name="application-list",
    ),
    path(
        "applications/<int:pk>",
        ApplicationDetail.as_view(),
        name="application-detail",
    ),
]
