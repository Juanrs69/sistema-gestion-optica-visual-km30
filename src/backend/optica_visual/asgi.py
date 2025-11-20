"""
ASGI config for optica_visual project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optica_visual.settings.development')

application = get_asgi_application()