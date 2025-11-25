"""
URLs para la API de productos
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet

# El router crea automáticamente todas las URLs del ViewSet
router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')

urlpatterns = [
    path('api/', include(router.urls)),
]

# Esto automáticamente crea estas URLs:
# GET    /api/productos/                     - Listar productos
# POST   /api/productos/                     - Crear producto
# GET    /api/productos/{id}/                - Ver producto específico  
# PUT    /api/productos/{id}/                - Actualizar producto completo
# PATCH  /api/productos/{id}/                - Actualizar parcialmente
# DELETE /api/productos/{id}/                - Eliminar producto
# GET    /api/productos/por_categoria/       - Agrupar por categoría
# GET    /api/productos/bajo_stock/          - Productos con poco stock
# GET    /api/productos/estadisticas/        - Dashboard de estadísticas
# PATCH  /api/productos/{id}/actualizar_stock/ - Solo actualizar stock
# POST   /api/productos/{id}/reducir_stock/  - Reducir stock (para ventas)