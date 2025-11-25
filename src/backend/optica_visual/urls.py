"""
URL Configuration para Óptica Visual Km 30
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),
    
    # APIs de las aplicaciones
    path('', include('apps.pacientes.urls')),
    
    # API de autenticación (JWT)
    path('api/auth/', include('rest_framework.urls')),
]

# Configuración para servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)