from django.db import models
from django.core.validators import RegexValidator


class Paciente(models.Model):
    """
    Modelo para almacenar información de pacientes de la óptica
    """
    
    TIPOS_DOCUMENTO = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
        ('PP', 'Pasaporte'),
        ('RC', 'Registro Civil'),
    ]
    
    # Información de identificación
    tipo_documento = models.CharField(
        max_length=2, 
        choices=TIPOS_DOCUMENTO, 
        default='CC',
        verbose_name='Tipo de Documento'
    )
    numero_documento = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name='Número de Documento',
        help_text='Número único de identificación del paciente'
    )
    
    # Información personal
    nombres = models.CharField(
        max_length=100,
        verbose_name='Nombres'
    )
    apellidos = models.CharField(
        max_length=100,
        verbose_name='Apellidos'
    )
    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de Nacimiento'
    )
    
    # Información de contacto
    telefono_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El teléfono debe tener entre 9 y 15 dígitos."
    )
    telefono = models.CharField(
        validators=[telefono_validator],
        max_length=17,
        blank=True,
        verbose_name='Teléfono'
    )
    email = models.EmailField(
        blank=True,
        verbose_name='Correo Electrónico'
    )
    direccion = models.TextField(
        blank=True,
        verbose_name='Dirección'
    )
    
    # Información adicional
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones Médicas',
        help_text='Información médica relevante del paciente'
    )
    
    # Campos de auditoría
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    class Meta:
        db_table = 'pacientes'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['numero_documento']),
            models.Index(fields=['nombres', 'apellidos']),
            models.Index(fields=['fecha_registro']),
        ]
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.numero_documento}"
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del paciente"""
        return f"{self.nombres} {self.apellidos}"
    
    @property
    def edad(self):
        """Calcula y retorna la edad del paciente"""
        from datetime import date
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
    
    def get_historial_prescripciones(self):
        """Retorna el historial de prescripciones del paciente"""
        return self.prescripciones.all().order_by('-fecha_examen')
    
    def get_facturas(self):
        """Retorna las facturas del paciente"""
        return self.facturas.all().order_by('-fecha')