"""
Configuración de Django para desarrollo
"""
from .base import *

# Configuraciones específicas de desarrollo
DEBUG = True

# Base de datos para desarrollo (SQLite por defecto)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Usar PostgreSQL si está configurado en .env
if config('DATABASE_URL', default=None):
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL')
        )
    }

# Configuración de email para desarrollo (consola)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Django Debug Toolbar (temporalmente deshabilitado)
# try:
#     import debug_toolbar
#     INSTALLED_APPS += ['debug_toolbar']
#     MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
#     INTERNAL_IPS = ['127.0.0.1', 'localhost']
# except ImportError:
#     pass

# Configuración de logs más verbose en desarrollo
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'optica_visual': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}