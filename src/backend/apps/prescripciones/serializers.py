from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Prescripcion, HistorialCambios
from apps.pacientes.models import Paciente


class PrescripcionSerializer(serializers.ModelSerializer):
    """
    Serializer completo para prescripciones oftalmológicas
    """
    # Campos calculados
    edad_paciente_en_examen = serializers.ReadOnlyField()
    es_vigente = serializers.ReadOnlyField()
    dias_hasta_vencimiento = serializers.ReadOnlyField()
    tiene_astigmatismo = serializers.ReadOnlyField()
    tiene_presbicia = serializers.ReadOnlyField()
    graduacion_od_completa = serializers.ReadOnlyField()
    graduacion_os_completa = serializers.ReadOnlyField()
    
    # Información del paciente y profesional
    paciente_nombre = serializers.CharField(source='paciente.nombre_completo', read_only=True)
    paciente_documento = serializers.CharField(source='paciente.numero_documento', read_only=True)
    profesional_nombre = serializers.CharField(source='profesional.get_full_name', read_only=True)
    
    class Meta:
        model = Prescripcion
        fields = [
            'id', 'numero_prescripcion', 'fecha_examen',
            'paciente', 'paciente_nombre', 'paciente_documento',
            'profesional', 'profesional_nombre',
            'od_esfera', 'od_cilindro', 'od_eje',
            'os_esfera', 'os_cilindro', 'os_eje',
            'adicion', 'distancia_pupilar',
            'agudeza_visual_od', 'agudeza_visual_os',
            'observaciones', 'tipo_lente_recomendado',
            'vigente', 'fecha_registro', 'fecha_actualizacion',
            # Campos calculados
            'edad_paciente_en_examen', 'es_vigente', 'dias_hasta_vencimiento',
            'tiene_astigmatismo', 'tiene_presbicia',
            'graduacion_od_completa', 'graduacion_os_completa'
        ]
        read_only_fields = ['id', 'numero_prescripcion', 'fecha_registro', 'fecha_actualizacion']
    
    def validate_fecha_examen(self, value):
        """Validar que la fecha de examen no sea futura"""
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("La fecha del examen no puede ser futura.")
        return value
    
    def validate_od_eje(self, value):
        """Validar eje del ojo derecho solo si hay cilindro"""
        # Esta validación se complementará en validate()
        return value
    
    def validate_os_eje(self, value):
        """Validar eje del ojo izquierdo solo si hay cilindro"""
        # Esta validación se complementará en validate()
        return value
    
    def validate(self, data):
        """Validaciones a nivel de objeto"""
        # Validar coherencia entre cilindro y eje
        if data.get('od_cilindro', 0) != 0 and data.get('od_eje', 0) == 0:
            raise serializers.ValidationError({
                'od_eje': 'El eje es obligatorio cuando hay cilindro en OD.'
            })
        
        if data.get('os_cilindro', 0) != 0 and data.get('os_eje', 0) == 0:
            raise serializers.ValidationError({
                'os_eje': 'El eje es obligatorio cuando hay cilindro en OS.'
            })
        
        # Validar adición según edad del paciente
        paciente = data.get('paciente')
        if paciente and data.get('adicion'):
            # Calcular edad aproximada
            from datetime import date
            fecha_examen = data.get('fecha_examen', date.today())
            edad_aprox = fecha_examen.year - paciente.fecha_nacimiento.year
            
            if edad_aprox < 40 and data.get('adicion', 0) > 0:
                # Advertencia, no error - puede ser presbicia temprana
                pass
        
        return data


class PrescripcionCreateSerializer(PrescripcionSerializer):
    """
    Serializer específico para creación de prescripciones
    """
    class Meta(PrescripcionSerializer.Meta):
        fields = [
            'paciente', 'fecha_examen',
            'od_esfera', 'od_cilindro', 'od_eje',
            'os_esfera', 'os_cilindro', 'os_eje',
            'adicion', 'distancia_pupilar',
            'agudeza_visual_od', 'agudeza_visual_os',
            'observaciones', 'tipo_lente_recomendado'
        ]


class PrescripcionListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listado de prescripciones
    """
    paciente_nombre = serializers.CharField(source='paciente.nombre_completo', read_only=True)
    profesional_nombre = serializers.CharField(source='profesional.get_full_name', read_only=True)
    es_vigente = serializers.ReadOnlyField()
    dias_hasta_vencimiento = serializers.ReadOnlyField()
    
    class Meta:
        model = Prescripcion
        fields = [
            'id', 'numero_prescripcion', 'fecha_examen',
            'paciente_nombre', 'profesional_nombre',
            'graduacion_od_completa', 'graduacion_os_completa',
            'es_vigente', 'dias_hasta_vencimiento', 'vigente'
        ]


class PrescripcionPacienteHistorialSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar historial de prescripciones de un paciente
    """
    profesional_nombre = serializers.CharField(source='profesional.get_full_name', read_only=True)
    graduacion_od = serializers.CharField(source='graduacion_od_completa', read_only=True)
    graduacion_os = serializers.CharField(source='graduacion_os_completa', read_only=True)
    diferencia_anterior = serializers.SerializerMethodField()
    
    class Meta:
        model = Prescripcion
        fields = [
            'id', 'numero_prescripcion', 'fecha_examen',
            'profesional_nombre', 'graduacion_od', 'graduacion_os',
            'tiene_astigmatismo', 'tiene_presbicia', 'es_vigente',
            'diferencia_anterior', 'observaciones'
        ]
    
    def get_diferencia_anterior(self, obj):
        """Obtener diferencia con prescripción anterior"""
        diferencia = obj.calcular_diferencia_con_anterior()
        if diferencia:
            return {
                'max_diferencia_dioptricas': diferencia['max_diferencia'],
                'meses_desde_anterior': diferencia['meses_transcurridos']
            }
        return None


class HistorialCambiosSerializer(serializers.ModelSerializer):
    """
    Serializer para el historial de cambios
    """
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
    
    class Meta:
        model = HistorialCambios
        fields = [
            'id', 'campo_modificado', 'valor_anterior', 'valor_nuevo',
            'usuario', 'usuario_nombre', 'fecha_cambio', 'motivo'
        ]
        read_only_fields = ['id', 'fecha_cambio']


class PrescripcionComparacionSerializer(serializers.Serializer):
    """
    Serializer para comparar dos prescripciones
    """
    prescripcion_1_id = serializers.IntegerField()
    prescripcion_2_id = serializers.IntegerField()
    
    def validate(self, data):
        """Validar que ambas prescripciones existan y sean del mismo paciente"""
        try:
            pres1 = Prescripcion.objects.get(id=data['prescripcion_1_id'])
            pres2 = Prescripcion.objects.get(id=data['prescripcion_2_id'])
        except Prescripcion.DoesNotExist:
            raise serializers.ValidationError("Una de las prescripciones no existe.")
        
        if pres1.paciente != pres2.paciente:
            raise serializers.ValidationError("Las prescripciones deben ser del mismo paciente.")
        
        return data