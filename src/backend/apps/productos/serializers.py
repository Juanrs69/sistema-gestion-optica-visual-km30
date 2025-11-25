"""
Serializers para la API de productos
"""
from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializer básico para productos - Convierte el modelo a JSON
    """
    # Campos calculados (solo lectura)
    margen_ganancia = serializers.ReadOnlyField()
    necesita_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Producto
        fields = '__all__'  # Todos los campos
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']

class ProductoListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar productos (menos información)
    """
    margen_ganancia = serializers.ReadOnlyField()
    necesita_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Producto
        fields = [
            'id', 
            'nombre', 
            'categoria', 
            'codigo',
            'precio_venta', 
            'stock',
            'margen_ganancia',
            'necesita_stock',
            'activo'
        ]

class ProductoCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear productos - Con validaciones específicas
    """
    
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'categoria', 
            'codigo',
            'precio_compra',
            'precio_venta',
            'stock',
            'stock_minimo',
            'descripcion',
            'activo'
        ]
    
    def validate_precio_venta(self, value):
        """Validar que el precio de venta sea mayor al de compra"""
        precio_compra = self.initial_data.get('precio_compra', 0)
        
        # Convertir a Decimal si es string
        if isinstance(precio_compra, str):
            from decimal import Decimal
            precio_compra = Decimal(precio_compra)
        
        if value <= precio_compra:
            raise serializers.ValidationError(
                "El precio de venta debe ser mayor al precio de compra"
            )
        return value
    
    def validate_codigo(self, value):
        """Validar código único solo si se proporciona"""
        if value and Producto.objects.filter(codigo=value).exists():
            raise serializers.ValidationError(
                "Ya existe un producto con este código"
            )
        return value

class ProductoStockSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar solo el stock
    """
    class Meta:
        model = Producto
        fields = ['stock']
    
    def validate_stock(self, value):
        """No permitir stock negativo"""
        if value < 0:
            raise serializers.ValidationError(
                "El stock no puede ser negativo"
            )
        return value