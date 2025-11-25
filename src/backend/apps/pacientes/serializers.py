from rest_framework import serializers
from django.core.validators import validate_email
from .models import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Paciente
    """
    nombre_completo = serializers.ReadOnlyField()
    edad = serializers.ReadOnlyField()
    
    class Meta:
        model = Paciente
        fields = [
            'id', 'tipo_documento', 'numero_documento',
            'nombres', 'apellidos', 'nombre_completo',
            'fecha_nacimiento', 'edad', 'telefono', 'email',
            'direccion', 'observaciones', 'activo',
            'fecha_registro', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_registro', 'fecha_actualizacion']
    
    def validate_numero_documento(self, value):
        """
        Valida que el número de documento sea único y tenga formato correcto
        """
        if not value.strip():
            raise serializers.ValidationError("El número de documento no puede estar vacío.")
        
        # Verificar unicidad solo si es un nuevo paciente o cambió el documento
        if self.instance is None or self.instance.numero_documento != value:
            if Paciente.objects.filter(numero_documento=value).exists():
                raise serializers.ValidationError("Ya existe un paciente con este número de documento.")
        
        return value.strip()
    
    def validate_email(self, value):
        """
        Valida el formato del email
        """
        if value:
            try:
                validate_email(value)
            except serializers.ValidationError:
                raise serializers.ValidationError("Ingrese un email válido.")
        return value
    
    def validate(self, data):
        """
        Validaciones a nivel de objeto
        """
        # Validar que los nombres y apellidos no estén vacíos
        if not data.get('nombres', '').strip():
            raise serializers.ValidationError({'nombres': 'Los nombres son obligatorios.'})
        
        if not data.get('apellidos', '').strip():
            raise serializers.ValidationError({'apellidos': 'Los apellidos son obligatorios.'})
        
        return data


class PacienteCreateSerializer(PacienteSerializer):
    """
    Serializer específico para creación de pacientes
    """
    class Meta(PacienteSerializer.Meta):
        fields = [
            'tipo_documento', 'numero_documento',
            'nombres', 'apellidos', 'fecha_nacimiento',
            'telefono', 'email', 'direccion', 'observaciones'
        ]


class PacienteListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listado de pacientes
    """
    nombre_completo = serializers.ReadOnlyField()
    edad = serializers.ReadOnlyField()
    
    class Meta:
        model = Paciente
        fields = [
            'id', 'numero_documento', 'nombre_completo',
            'telefono', 'email', 'edad', 'fecha_registro'
        ]