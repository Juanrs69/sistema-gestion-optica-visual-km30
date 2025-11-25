from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Paciente
from .serializers import PacienteSerializer, PacienteCreateSerializer, PacienteListSerializer


class PacienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión completa de pacientes
    """
    queryset = Paciente.objects.filter(activo=True)
    serializer_class = PacienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_documento', 'activo']
    search_fields = ['numero_documento', 'nombres', 'apellidos', 'email']
    ordering_fields = ['fecha_registro', 'nombres', 'apellidos', 'numero_documento']
    ordering = ['-fecha_registro']
    
    def get_serializer_class(self):
        """
        Retorna el serializer apropiado según la acción
        """
        if self.action == 'create':
            return PacienteCreateSerializer
        elif self.action == 'list':
            return PacienteListSerializer
        return PacienteSerializer
    
    def get_queryset(self):
        """
        Personaliza el queryset según los parámetros de consulta
        """
        queryset = Paciente.objects.all()
        
        # Filtro por estado activo (por defecto solo activos)
        activo = self.request.query_params.get('activo', 'true')
        if activo.lower() == 'false':
            queryset = queryset.filter(activo=False)
        elif activo.lower() == 'true':
            queryset = queryset.filter(activo=True)
        
        # Filtro por edad
        edad_min = self.request.query_params.get('edad_min')
        edad_max = self.request.query_params.get('edad_max')
        
        if edad_min or edad_max:
            from datetime import date, timedelta
            today = date.today()
            
            if edad_max:
                fecha_min = today - timedelta(days=int(edad_max) * 365.25 + 365)
                queryset = queryset.filter(fecha_nacimiento__gte=fecha_min)
            
            if edad_min:
                fecha_max = today - timedelta(days=int(edad_min) * 365.25)
                queryset = queryset.filter(fecha_nacimiento__lte=fecha_max)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        """
        Desactiva un paciente sin eliminarlo físicamente
        """
        paciente = self.get_object()
        paciente.activo = False
        paciente.save()
        
        return Response({
            'mensaje': f'Paciente {paciente.nombre_completo} desactivado correctamente.'
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        """
        Reactiva un paciente
        """
        paciente = self.get_object()
        paciente.activo = True
        paciente.save()
        
        return Response({
            'mensaje': f'Paciente {paciente.nombre_completo} activado correctamente.'
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def historial_prescripciones(self, request, pk=None):
        """
        Retorna el historial de prescripciones del paciente
        """
        paciente = self.get_object()
        prescripciones = paciente.get_historial_prescripciones()
        
        # Aquí se usará el serializer de prescripciones cuando esté creado
        return Response({
            'paciente': paciente.nombre_completo,
            'total_prescripciones': prescripciones.count(),
            'mensaje': 'Historial de prescripciones (pendiente implementar serializer)'
        })
    
    @action(detail=True, methods=['get'])
    def facturas(self, request, pk=None):
        """
        Retorna las facturas del paciente
        """
        paciente = self.get_object()
        facturas = paciente.get_facturas()
        
        # Aquí se usará el serializer de facturas cuando esté creado
        return Response({
            'paciente': paciente.nombre_completo,
            'total_facturas': facturas.count(),
            'mensaje': 'Facturas del paciente (pendiente implementar serializer)'
        })
    
    @action(detail=False, methods=['get'])
    def busqueda_avanzada(self, request):
        """
        Búsqueda avanzada de pacientes
        """
        query = request.query_params.get('q', '')
        
        if not query:
            return Response({
                'error': 'Parámetro de búsqueda "q" requerido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Búsqueda por múltiples campos
        pacientes = Paciente.objects.filter(
            Q(numero_documento__icontains=query) |
            Q(nombres__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(email__icontains=query) |
            Q(telefono__icontains=query)
        ).filter(activo=True)
        
        serializer = PacienteListSerializer(pacientes, many=True)
        return Response({
            'total': pacientes.count(),
            'resultados': serializer.data
        })