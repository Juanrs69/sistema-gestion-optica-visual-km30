from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from apps.pacientes.models import Paciente


class Prescripcion(models.Model):
    """
    Modelo para almacenar prescripciones oftalmológicas (fórmulas visuales)
    """
    
    # Relaciones
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='prescripciones',
        verbose_name='Paciente'
    )
    profesional = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='prescripciones_creadas',
        verbose_name='Profesional que realiza el examen'
    )
    
    # Información del examen
    fecha_examen = models.DateField(
        verbose_name='Fecha del Examen'
    )
    numero_prescripcion = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Prescripción',
        help_text='Número único generado automáticamente'
    )
    
    # Medidas Ojo Derecho (OD)
    od_esfera = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(-20.00), MaxValueValidator(20.00)],
        verbose_name='OD Esfera',
        help_text='Ojo Derecho - Esfera (-20.00 a +20.00)'
    )
    od_cilindro = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(-6.00), MaxValueValidator(6.00)],
        default=0.00,
        verbose_name='OD Cilindro',
        help_text='Ojo Derecho - Cilindro (-6.00 a +6.00)'
    )
    od_eje = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(180)],
        default=0,
        verbose_name='OD Eje',
        help_text='Ojo Derecho - Eje (0° a 180°)'
    )
    
    # Medidas Ojo Izquierdo (OS)
    os_esfera = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(-20.00), MaxValueValidator(20.00)],
        verbose_name='OS Esfera',
        help_text='Ojo Izquierdo - Esfera (-20.00 a +20.00)'
    )
    os_cilindro = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(-6.00), MaxValueValidator(6.00)],
        default=0.00,
        verbose_name='OS Cilindro',
        help_text='Ojo Izquierdo - Cilindro (-6.00 a +6.00)'
    )
    os_eje = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(180)],
        default=0,
        verbose_name='OS Eje',
        help_text='Ojo Izquierdo - Eje (0° a 180°)'
    )
    
    # Medidas adicionales
    adicion = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.00), MaxValueValidator(4.00)],
        null=True,
        blank=True,
        verbose_name='Adición',
        help_text='Para presbicia (0.00 a +4.00)'
    )
    distancia_pupilar = models.PositiveIntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(80)],
        null=True,
        blank=True,
        verbose_name='Distancia Pupilar (mm)',
        help_text='Distancia entre pupilas en milímetros'
    )
    
    # Información clínica adicional
    agudeza_visual_od = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Agudeza Visual OD',
        help_text='Ej: 20/20, 20/40'
    )
    agudeza_visual_os = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Agudeza Visual OS',
        help_text='Ej: 20/20, 20/40'
    )
    
    # Observaciones y recomendaciones
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones Médicas',
        help_text='Observaciones del examen, recomendaciones especiales'
    )
    tipo_lente_recomendado = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Tipo de Lente Recomendado',
        help_text='Ej: Monofocal, Bifocal, Progresivo'
    )
    
    # Control de vigencia
    vigente = models.BooleanField(
        default=True,
        verbose_name='Vigente',
        help_text='Las prescripciones tienen vigencia de 2 años'
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
    
    class Meta:
        db_table = 'prescripciones'
        verbose_name = 'Prescripción Oftalmológica'
        verbose_name_plural = 'Prescripciones Oftalmológicas'
        ordering = ['-fecha_examen', '-fecha_registro']
        indexes = [
            models.Index(fields=['paciente', '-fecha_examen']),
            models.Index(fields=['numero_prescripcion']),
            models.Index(fields=['vigente', '-fecha_examen']),
            models.Index(fields=['profesional', '-fecha_registro']),
        ]
    
    def __str__(self):
        return f"Prescripción {self.numero_prescripcion} - {self.paciente.nombre_completo} ({self.fecha_examen})"
    
    def save(self, *args, **kwargs):
        """Generar número de prescripción automáticamente"""
        if not self.numero_prescripcion:
            # Formato: PRES-YYYY-NNNN
            from datetime import date
            year = date.today().year
            last_prescription = Prescripcion.objects.filter(
                numero_prescripcion__startswith=f'PRES-{year}-'
            ).order_by('-numero_prescripcion').first()
            
            if last_prescription:
                last_number = int(last_prescription.numero_prescripcion.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.numero_prescripcion = f'PRES-{year}-{new_number:04d}'
        
        super().save(*args, **kwargs)
    
    @property
    def edad_paciente_en_examen(self):
        """Edad del paciente al momento del examen"""
        from datetime import date
        if self.fecha_examen and self.paciente.fecha_nacimiento:
            return self.fecha_examen.year - self.paciente.fecha_nacimiento.year - (
                (self.fecha_examen.month, self.fecha_examen.day) < 
                (self.paciente.fecha_nacimiento.month, self.paciente.fecha_nacimiento.day)
            )
        return None
    
    @property
    def es_vigente(self):
        """Verifica si la prescripción está vigente (2 años)"""
        from datetime import date, timedelta
        if not self.vigente:
            return False
        fecha_vencimiento = self.fecha_examen + timedelta(days=730)  # 2 años
        return date.today() <= fecha_vencimiento
    
    @property
    def dias_hasta_vencimiento(self):
        """Días restantes hasta el vencimiento"""
        from datetime import date, timedelta
        if not self.vigente:
            return 0
        fecha_vencimiento = self.fecha_examen + timedelta(days=730)
        diferencia = fecha_vencimiento - date.today()
        return max(0, diferencia.days)
    
    @property
    def tiene_astigmatismo(self):
        """Verifica si el paciente tiene astigmatismo"""
        return self.od_cilindro != 0 or self.os_cilindro != 0
    
    @property
    def tiene_presbicia(self):
        """Verifica si requiere corrección para presbicia"""
        return self.adicion is not None and self.adicion > 0
    
    @property
    def graduacion_od_completa(self):
        """Graduación completa del ojo derecho en formato estándar"""
        resultado = f"Esf: {self.od_esfera:+.2f}"
        if self.od_cilindro != 0:
            resultado += f" Cil: {self.od_cilindro:+.2f} Eje: {self.od_eje}°"
        if self.adicion:
            resultado += f" Add: +{self.adicion:.2f}"
        return resultado
    
    @property
    def graduacion_os_completa(self):
        """Graduación completa del ojo izquierdo en formato estándar"""
        resultado = f"Esf: {self.os_esfera:+.2f}"
        if self.os_cilindro != 0:
            resultado += f" Cil: {self.os_cilindro:+.2f} Eje: {self.os_eje}°"
        if self.adicion:
            resultado += f" Add: +{self.adicion:.2f}"
        return resultado
    
    def calcular_diferencia_con_anterior(self):
        """Calcula la diferencia con la prescripción anterior"""
        anterior = Prescripcion.objects.filter(
            paciente=self.paciente,
            fecha_examen__lt=self.fecha_examen,
            vigente=True
        ).order_by('-fecha_examen').first()
        
        if not anterior:
            return None
        
        diferencias = {
            'od_esfera': abs(float(self.od_esfera) - float(anterior.od_esfera)),
            'od_cilindro': abs(float(self.od_cilindro) - float(anterior.od_cilindro)),
            'os_esfera': abs(float(self.os_esfera) - float(anterior.os_esfera)),
            'os_cilindro': abs(float(self.os_cilindro) - float(anterior.os_cilindro)),
            'meses_transcurridos': (self.fecha_examen - anterior.fecha_examen).days // 30
        }
        
        # Diferencia máxima
        diferencias['max_diferencia'] = max(
            diferencias['od_esfera'], diferencias['od_cilindro'],
            diferencias['os_esfera'], diferencias['os_cilindro']
        )
        
        return diferencias
    
    def invalidar_prescripciones_anteriores(self):
        """Marca como no vigentes las prescripciones anteriores del mismo paciente"""
        Prescripcion.objects.filter(
            paciente=self.paciente,
            vigente=True
        ).exclude(id=self.id).update(vigente=False)


class HistorialCambios(models.Model):
    """
    Modelo para llevar un historial de cambios en prescripciones
    """
    
    prescripcion = models.ForeignKey(
        Prescripcion,
        on_delete=models.CASCADE,
        related_name='historial_cambios'
    )
    campo_modificado = models.CharField(max_length=50)
    valor_anterior = models.CharField(max_length=100)
    valor_nuevo = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(blank=True)
    
    class Meta:
        db_table = 'historial_cambios_prescripciones'
        verbose_name = 'Historial de Cambio'
        verbose_name_plural = 'Historial de Cambios'
        ordering = ['-fecha_cambio']