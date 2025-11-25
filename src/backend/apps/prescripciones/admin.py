from django.contrib import admin
from .models import Prescripcion, HistorialCambios


@admin.register(Prescripcion)
class PrescripcionAdmin(admin.ModelAdmin):
    list_display = (
        'numero_prescripcion', 'paciente', 'fecha_examen', 
        'profesional', 'es_vigente', 'tiene_astigmatismo', 'tiene_presbicia'
    )
    list_filter = (
        'vigente', 'fecha_examen', 'profesional', 'tipo_lente_recomendado'
    )
    search_fields = (
        'numero_prescripcion', 'paciente__nombres', 'paciente__apellidos',
        'paciente__numero_documento', 'profesional__first_name', 'profesional__last_name'
    )
    readonly_fields = (
        'numero_prescripcion', 'fecha_registro', 'fecha_actualizacion',
        'edad_paciente_en_examen', 'es_vigente', 'dias_hasta_vencimiento',
        'graduacion_od_completa', 'graduacion_os_completa'
    )
    
    fieldsets = (
        ('Información General', {
            'fields': (
                'numero_prescripcion', 'paciente', 'profesional', 'fecha_examen'
            )
        }),
        ('Graduación Ojo Derecho (OD)', {
            'fields': ('od_esfera', 'od_cilindro', 'od_eje', 'agudeza_visual_od'),
            'classes': ('collapse',)
        }),
        ('Graduación Ojo Izquierdo (OS)', {
            'fields': ('os_esfera', 'os_cilindro', 'os_eje', 'agudeza_visual_os'),
            'classes': ('collapse',)
        }),
        ('Información Adicional', {
            'fields': ('adicion', 'distancia_pupilar', 'tipo_lente_recomendado'),
            'classes': ('collapse',)
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
        ('Control', {
            'fields': ('vigente',)
        }),
        ('Información del Sistema', {
            'fields': (
                'fecha_registro', 'fecha_actualizacion',
                'edad_paciente_en_examen', 'es_vigente', 'dias_hasta_vencimiento'
            ),
            'classes': ('collapse',)
        }),
        ('Graduación Completa (Solo Lectura)', {
            'fields': ('graduacion_od_completa', 'graduacion_os_completa'),
            'classes': ('collapse',)
        })
    )
    
    date_hierarchy = 'fecha_examen'
    ordering = ('-fecha_examen', '-fecha_registro')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('paciente', 'profesional')


@admin.register(HistorialCambios)
class HistorialCambiosAdmin(admin.ModelAdmin):
    list_display = (
        'prescripcion', 'campo_modificado', 'valor_anterior', 
        'valor_nuevo', 'usuario', 'fecha_cambio'
    )
    list_filter = ('campo_modificado', 'usuario', 'fecha_cambio')
    search_fields = (
        'prescripcion__numero_prescripcion', 'prescripcion__paciente__nombres',
        'campo_modificado', 'usuario__username'
    )
    readonly_fields = ('fecha_cambio',)
    
    fieldsets = (
        ('Información del Cambio', {
            'fields': ('prescripcion', 'campo_modificado', 'valor_anterior', 'valor_nuevo')
        }),
        ('Información de Auditoría', {
            'fields': ('usuario', 'fecha_cambio', 'motivo')
        })
    )
    
    date_hierarchy = 'fecha_cambio'
    ordering = ('-fecha_cambio',)
    
    def has_add_permission(self, request):
        # Los cambios se registran automáticamente
        return False
    
    def has_change_permission(self, request, obj=None):
        # No se pueden modificar los registros de auditoría
        return False
    
    def has_delete_permission(self, request, obj=None):
        # No se pueden eliminar registros de auditoría
        return False