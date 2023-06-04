from django.apps import AppConfig

from dev_bridge_admin.settings import DEFAULT_AUTO_FIELD


class EmailsConfig(AppConfig):
    default_auto_field = DEFAULT_AUTO_FIELD
    name = "emails"
    verbose_name = "письма"
