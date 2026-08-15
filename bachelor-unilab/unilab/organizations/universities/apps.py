from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UniversitiesConfig(AppConfig):
    name = "unilab.organizations.universities"
    verbose_name = _("Universities")

    def ready(self):
        try:
            import unilab.organizations.universities.signals  # noqa F401
        except ImportError:
            pass
