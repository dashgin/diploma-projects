from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersMetadataConfig(AppConfig):
    name = "unilab.users_metadata"
    verbose_name = _("Users Metadata")

    def ready(self):
        try:
            import unilab.users_metadata.signals  # noqa F401
        except ImportError:
            pass
