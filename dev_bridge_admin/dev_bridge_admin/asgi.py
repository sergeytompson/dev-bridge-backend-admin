import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dev_bridge_admin.settings")

application = get_asgi_application()
