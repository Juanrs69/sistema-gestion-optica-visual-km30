from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PacienteViewSet

# Configuración del router para las vistas basadas en ViewSet
router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet, basename='paciente')

# URLs de la aplicación
urlpatterns = [
    # API endpoints para pacientes
    path('api/', include(router.urls)),
]