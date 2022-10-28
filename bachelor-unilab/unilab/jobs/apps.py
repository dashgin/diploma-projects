from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "unilab.jobs"
    verbose_name = _("Jobs")

    def ready(self):
        try:
            import unilab.jobs.signals  # noqa F401
        except ImportError:
            pass
