from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CompaniesConfig(AppConfig):
    name = "unilab.organizations.companies"
    verbose_name = _("Companies")

    def ready(self):
        try:
            import unilab.organizations.companies.signals  # noqa F401
        except ImportError:
            pass
