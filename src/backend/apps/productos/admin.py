"""
Configuración del admin para productos
"""
from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """
    Configuración para ver productos en el admin de Django
    """
    # Qué columnas se ven en la lista
    list_display = [
        'nombre', 
        'categoria', 
        'codigo', 
        'precio_venta', 
        'stock',
        'necesita_stock',
        'activo'
    ]
    
    # Por qué campos puedes filtrar
    list_filter = ['categoria', 'activo', 'fecha_creacion']
    
    # En qué campos puedes buscar
    search_fields = ['nombre', 'codigo', 'descripcion']
    
    # Campos que se pueden editar directamente en la lista
    list_editable = ['precio_venta', 'stock', 'activo']
    
    # Cómo agrupar los campos en el formulario
    fieldsets = [
        ('Información Básica', {
            'fields': ['nombre', 'categoria', 'codigo', 'descripcion']
        }),
        ('Precios', {
            'fields': ['precio_compra', 'precio_venta']
        }),
        ('Inventario', {
            'fields': ['stock', 'stock_minimo']
        }),
        ('Estado', {
            'fields': ['activo']
        }),
    ]
    
    # Campos que son solo de lectura
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']