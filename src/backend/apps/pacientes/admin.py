from django.contrib import admin
from .models import Paciente


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = (
        'numero_documento', 'nombres', 'apellidos', 
        'telefono', 'email', 'fecha_registro'
    )
    list_filter = ('tipo_documento', 'fecha_registro', 'fecha_nacimiento')
    search_fields = ('numero_documento', 'nombres', 'apellidos', 'email')
    readonly_fields = ('fecha_registro', 'fecha_actualizacion')
    
    fieldsets = (
        ('Información Personal', {
            'fields': (
                'tipo_documento', 'numero_documento',
                'nombres', 'apellidos', 'fecha_nacimiento'
            )
        }),
        ('Información de Contacto', {
            'fields': ('telefono', 'email', 'direccion')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        })
    )
    
    ordering = ('-fecha_registro',)
    date_hierarchy = 'fecha_registro'