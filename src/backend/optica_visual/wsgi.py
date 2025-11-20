"""
WSGI config for optica_visual project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optica_visual.settings.development')

application = get_wsgi_application()