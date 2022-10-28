from django.urls import path

app_name = "users"
urlpatterns = [
    path(
        "users",
        UserList.as_view(),
        name="user-list",
    ),
    path(
        "users/<int:pk>",
        UserDetail.as_view(),
        name="user-detail",
    ),
    path(
        "change-password",
        UpdatePassword.as_view(),
        name="updatepassword",
    ),
]
