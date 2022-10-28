from unilab.jobs.urls import urlpatterns as jobs_urls
from unilab.organizations.urls import urlpatterns as organizations_urls
from unilab.posts.urls import urlpatterns as posts_urls
from unilab.users.urls import urlpatterns as users_urls
from unilab.users_metadata.urls import urlpatterns as users_metadata_urls

app_name = "api"


urlpatterns = (
    users_urls + users_metadata_urls + organizations_urls + jobs_urls + posts_urls
)
