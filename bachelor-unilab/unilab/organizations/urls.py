from unilab.organizations.companies.urls import urlpatterns as companies_urls
from unilab.organizations.universities.urls import urlpatterns as organizations_urls

urlpatterns = companies_urls + organizations_urls
