from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PostsConfig(AppConfig):
    name = "unilab.posts"
    verbose_name = _("Posts")

    def ready(self):
        try:
            import unilab.posts.signals  # noqa F401
        except ImportError:
            pass
