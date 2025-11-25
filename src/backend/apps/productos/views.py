"""
Vistas para la API de productos
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Avg, Count, F
from .models import Producto
from .serializers import (
    ProductoSerializer, 
    ProductoListSerializer, 
    ProductoCreateSerializer,
    ProductoStockSerializer
)

class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para gestionar productos
    Automáticamente crea endpoints para: GET, POST, PUT, DELETE
    """
    queryset = Producto.objects.all()
    
    # Filtros y búsqueda
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categoria', 'activo']  # Filtrar por categoría y estado
    search_fields = ['nombre', 'codigo', 'descripcion']  # Buscar en estos campos
    ordering_fields = ['nombre', 'precio_venta', 'stock', 'fecha_creacion']
    ordering = ['categoria', 'nombre']  # Orden por defecto
    
    def get_serializer_class(self):
        """
        Usar diferentes serializers según la acción
        """
        if self.action == 'list':
            return ProductoListSerializer
        elif self.action == 'create':
            return ProductoCreateSerializer
        elif self.action == 'actualizar_stock':
            return ProductoStockSerializer
        return ProductoSerializer
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """
        Endpoint personalizado: /api/productos/por_categoria/
        Agrupa productos por categoría
        """
        categorias = {}
        for categoria, nombre in Producto.CATEGORIA_CHOICES:
            productos = Producto.objects.filter(categoria=categoria, activo=True)
            if productos.exists():
                serializer = ProductoListSerializer(productos, many=True)
                categorias[nombre] = serializer.data
        
        return Response(categorias)
    
    @action(detail=False, methods=['get'])
    def bajo_stock(self, request):
        """
        Endpoint: /api/productos/bajo_stock/
        Productos que necesitan reposición
        """
        productos = Producto.objects.filter(
            stock__lte=F('stock_minimo'),
            activo=True
        )
        serializer = ProductoListSerializer(productos, many=True)
        return Response({
            'total': productos.count(),
            'productos': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Endpoint: /api/productos/estadisticas/
        Estadísticas del inventario
        """
        stats = {
            'resumen': {
                'total_productos': Producto.objects.filter(activo=True).count(),
                'valor_inventario': Producto.objects.aggregate(
                    total=Sum('precio_compra') * Sum('stock')
                )['total'] or 0,
                'productos_sin_stock': Producto.objects.filter(stock=0).count(),
                'productos_bajo_stock': Producto.objects.filter(
                    stock__lte=F('stock_minimo')
                ).count(),
            },
            'por_categoria': []
        }
        
        # Estadísticas por categoría
        for categoria, nombre in Producto.CATEGORIA_CHOICES:
            productos = Producto.objects.filter(categoria=categoria, activo=True)
            if productos.exists():
                stats['por_categoria'].append({
                    'categoria': nombre,
                    'total': productos.count(),
                    'stock_total': productos.aggregate(Sum('stock'))['stock__sum'] or 0,
                    'precio_promedio': productos.aggregate(Avg('precio_venta'))['precio_venta__avg'] or 0
                })
        
        return Response(stats)
    
    @action(detail=True, methods=['patch'])
    def actualizar_stock(self, request, pk=None):
        """
        Endpoint: /api/productos/{id}/actualizar_stock/
        Actualizar solo el stock de un producto
        """
        producto = self.get_object()
        serializer = ProductoStockSerializer(producto, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'mensaje': f'Stock actualizado para {producto.nombre}',
                'stock_anterior': producto.stock,
                'stock_nuevo': serializer.validated_data['stock']
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def reducir_stock(self, request, pk=None):
        """
        Endpoint: /api/productos/{id}/reducir_stock/
        Reducir stock cuando se vende un producto
        """
        producto = self.get_object()
        cantidad = request.data.get('cantidad', 1)
        
        if producto.reducir_stock(cantidad):
            return Response({
                'mensaje': f'Stock reducido en {cantidad} unidades',
                'stock_actual': producto.stock
            })
        else:
            return Response({
                'error': 'No hay suficiente stock disponible'
            }, status=status.HTTP_400_BAD_REQUEST)