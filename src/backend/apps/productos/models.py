"""
Modelos para el manejo de productos de la óptica
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Producto(models.Model):
    """
    Modelo para productos de la óptica (monturas, lentes, accesorios)
    """
    
    # TIPOS DE PRODUCTOS - Aquí defines las categorías
    CATEGORIA_CHOICES = [
        ('MONTURA', 'Montura'),
        ('LENTE', 'Lente'),
        ('ACCESORIO', 'Accesorio'),
        ('LIMPIEZA', 'Producto de Limpieza'),
        ('ESTUCHE', 'Estuche'),
        ('OTROS', 'Otros'),
    ]
    
    # CAMPOS BÁSICOS - Información que SÍ o SÍ necesitas
    nombre = models.CharField(
        max_length=200, 
        help_text="Ej: Montura Metal Dorada, Lente Antireflejo"
    )
    
    categoria = models.CharField(
        max_length=20, 
        choices=CATEGORIA_CHOICES,
        help_text="Tipo de producto"
    )
    
    # CÓDIGO - Solo para lentes y algunos productos específicos
    codigo = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        unique=True,  # No puede repetirse
        help_text="Código del producto (opcional, principalmente para lentes)"
    )
    
    # PRECIOS - Lo más importante para el negocio
    precio_compra = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Precio al que compraste el producto"
    )
    
    precio_venta = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Precio al que vendes el producto"
    )
    
    # INVENTARIO - Para saber cuántos tienes
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad disponible en inventario"
    )
    
    stock_minimo = models.PositiveIntegerField(
        default=1,
        help_text="Cantidad mínima antes de hacer pedido"
    )
    
    # INFORMACIÓN ADICIONAL
    descripcion = models.TextField(
        blank=True, 
        null=True,
        help_text="Descripción detallada del producto"
    )
    
    activo = models.BooleanField(
        default=True,
        help_text="Si el producto está disponible para venta"
    )
    
    # FECHAS - Para llevar control
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['categoria', 'nombre']  # Cómo se ordenan
        indexes = [
            models.Index(fields=['categoria']),
            models.Index(fields=['codigo']),
            models.Index(fields=['activo']),
        ]
    
    def __str__(self):
        """Cómo se ve el producto en el admin"""
        if self.codigo:
            return f"{self.codigo} - {self.nombre}"
        return self.nombre
    
    @property
    def margen_ganancia(self):
        """Calcula cuánto ganas por producto"""
        if self.precio_compra > 0:
            return ((self.precio_venta - self.precio_compra) / self.precio_compra) * 100
        return 0
    
    @property
    def necesita_stock(self):
        """Verifica si necesitas comprar más"""
        return self.stock <= self.stock_minimo
    
    def reducir_stock(self, cantidad):
        """Reduce el stock cuando vendes"""
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
            return True
        return False