from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrescripcionViewSet, HistorialCambiosViewSet

# Configuración del router
router = DefaultRouter()
router.register(r'prescripciones', PrescripcionViewSet, basename='prescripcion')
router.register(r'historial-cambios', HistorialCambiosViewSet, basename='historial-cambios')

# URLs de la aplicación
urlpatterns = [
    # API endpoints para prescripciones
    path('api/', include(router.urls)),
]