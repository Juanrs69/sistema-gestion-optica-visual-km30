from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from datetime import date, timedelta
from .models import Prescripcion, HistorialCambios
from .serializers import (
    PrescripcionSerializer, PrescripcionCreateSerializer, 
    PrescripcionListSerializer, PrescripcionPacienteHistorialSerializer,
    HistorialCambiosSerializer, PrescripcionComparacionSerializer
)
from apps.pacientes.models import Paciente


class PrescripcionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión completa de prescripciones oftalmológicas
    """
    queryset = Prescripcion.objects.all()
    serializer_class = PrescripcionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vigente', 'profesional', 'paciente']
    search_fields = [
        'numero_prescripcion', 'paciente__nombres', 'paciente__apellidos',
        'paciente__numero_documento', 'profesional__first_name', 'profesional__last_name'
    ]
    ordering_fields = ['fecha_examen', 'fecha_registro', 'numero_prescripcion']
    ordering = ['-fecha_examen', '-fecha_registro']
    
    def get_serializer_class(self):
        """Retorna el serializer apropiado según la acción"""
        if self.action == 'create':
            return PrescripcionCreateSerializer
        elif self.action == 'list':
            return PrescripcionListSerializer
        elif self.action == 'historial_paciente':
            return PrescripcionPacienteHistorialSerializer
        return PrescripcionSerializer
    
    def get_queryset(self):
        """Personaliza el queryset según parámetros"""
        queryset = Prescripcion.objects.select_related('paciente', 'profesional')
        
        # Filtro por vigencia
        vigentes_solo = self.request.query_params.get('vigentes_solo', None)
        if vigentes_solo and vigentes_solo.lower() == 'true':
            # Filtrar por vigencia real (no solo el campo booleano)
            fecha_limite = date.today() - timedelta(days=730)  # 2 años atrás
            queryset = queryset.filter(vigente=True, fecha_examen__gte=fecha_limite)
        
        # Filtro por rango de fechas
        fecha_desde = self.request.query_params.get('fecha_desde', None)
        fecha_hasta = self.request.query_params.get('fecha_hasta', None)
        
        if fecha_desde:
            queryset = queryset.filter(fecha_examen__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_examen__lte=fecha_hasta)
        
        # Filtro por tipo de problema visual
        tiene_astigmatismo = self.request.query_params.get('astigmatismo', None)
        if tiene_astigmatismo:
            if tiene_astigmatismo.lower() == 'true':
                queryset = queryset.filter(
                    Q(od_cilindro__gt=0) | Q(od_cilindro__lt=0) | 
                    Q(os_cilindro__gt=0) | Q(os_cilindro__lt=0)
                )
            else:
                queryset = queryset.filter(od_cilindro=0, os_cilindro=0)
        
        tiene_presbicia = self.request.query_params.get('presbicia', None)
        if tiene_presbicia:
            if tiene_presbicia.lower() == 'true':
                queryset = queryset.filter(adicion__gt=0)
            else:
                queryset = queryset.filter(Q(adicion__isnull=True) | Q(adicion=0))
        
        return queryset
    
    def perform_create(self, serializer):
        """Configuraciones adicionales al crear prescripción"""
        # Asignar el usuario actual como profesional
        serializer.save(profesional=self.request.user)
        
        # Invalidar prescripciones anteriores del mismo paciente
        prescripcion = serializer.instance
        prescripcion.invalidar_prescripciones_anteriores()
    
    def perform_update(self, serializer):
        """Registrar cambios en el historial"""
        # Obtener valores anteriores
        prescripcion_anterior = Prescripcion.objects.get(id=serializer.instance.id)
        
        # Guardar cambios
        serializer.save()
        
        # Registrar en historial (solo campos principales)
        campos_importantes = [
            'od_esfera', 'od_cilindro', 'od_eje',
            'os_esfera', 'os_cilindro', 'os_eje',
            'adicion', 'distancia_pupilar'
        ]
        
        for campo in campos_importantes:
            valor_anterior = getattr(prescripcion_anterior, campo)
            valor_nuevo = getattr(serializer.instance, campo)
            
            if valor_anterior != valor_nuevo:
                HistorialCambios.objects.create(
                    prescripcion=serializer.instance,
                    campo_modificado=campo,
                    valor_anterior=str(valor_anterior),
                    valor_nuevo=str(valor_nuevo),
                    usuario=self.request.user
                )
    
    @action(detail=False, methods=['get'])
    def vigentes(self, request):
        """Obtener solo prescripciones vigentes"""
        fecha_limite = date.today() - timedelta(days=730)
        prescripciones = Prescripcion.objects.filter(
            vigente=True,
            fecha_examen__gte=fecha_limite
        ).select_related('paciente', 'profesional')
        
        serializer = PrescripcionListSerializer(prescripciones, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_vencer(self, request):
        """Prescripciones que vencen en los próximos 90 días"""
        fecha_limite_inferior = date.today() - timedelta(days=640)  # Vencen en 90 días
        fecha_limite_superior = date.today() - timedelta(days=730)  # Ya vencidas
        
        prescripciones = Prescripcion.objects.filter(
            vigente=True,
            fecha_examen__gte=fecha_limite_superior,
            fecha_examen__lte=fecha_limite_inferior
        ).select_related('paciente', 'profesional')
        
        serializer = PrescripcionListSerializer(prescripciones, many=True)
        return Response({
            'total': prescripciones.count(),
            'prescripciones': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='paciente/(?P<paciente_id>[^/.]+)')
    def historial_paciente(self, request, paciente_id=None):
        """Obtener historial completo de prescripciones de un paciente"""
        try:
            paciente = Paciente.objects.get(id=paciente_id)
        except Paciente.DoesNotExist:
            return Response(
                {'error': 'Paciente no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        prescripciones = Prescripcion.objects.filter(
            paciente=paciente
        ).select_related('profesional').order_by('-fecha_examen')
        
        serializer = PrescripcionPacienteHistorialSerializer(prescripciones, many=True)
        
        # Información adicional del paciente
        data = {
            'paciente': {
                'id': paciente.id,
                'nombre_completo': paciente.nombre_completo,
                'numero_documento': paciente.numero_documento,
                'edad_actual': paciente.edad
            },
            'total_prescripciones': prescripciones.count(),
            'prescripcion_actual': None,
            'historial': serializer.data
        }
        
        # Identificar prescripción actual (vigente más reciente)
        prescripcion_actual = prescripciones.filter(vigente=True).first()
        if prescripcion_actual:
            data['prescripcion_actual'] = PrescripcionSerializer(prescripcion_actual).data
        
        return Response(data)
    
    @action(detail=False, methods=['post'])
    def comparar(self, request):
        """Comparar dos prescripciones del mismo paciente"""
        serializer = PrescripcionComparacionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        pres1 = Prescripcion.objects.get(id=serializer.validated_data['prescripcion_1_id'])
        pres2 = Prescripcion.objects.get(id=serializer.validated_data['prescripcion_2_id'])
        
        # Calcular diferencias
        comparacion = {
            'prescripcion_1': PrescripcionSerializer(pres1).data,
            'prescripcion_2': PrescripcionSerializer(pres2).data,
            'diferencias': {
                'od_esfera': float(pres2.od_esfera) - float(pres1.od_esfera),
                'od_cilindro': float(pres2.od_cilindro) - float(pres1.od_cilindro),
                'od_eje': pres2.od_eje - pres1.od_eje,
                'os_esfera': float(pres2.os_esfera) - float(pres1.os_esfera),
                'os_cilindro': float(pres2.os_cilindro) - float(pres1.os_cilindro),
                'os_eje': pres2.os_eje - pres1.os_eje,
                'meses_transcurridos': (pres2.fecha_examen - pres1.fecha_examen).days // 30
            },
            'analisis': {
                'cambio_significativo': False,
                'recomendaciones': []
            }
        }
        
        # Análisis automático
        max_diferencia = max(
            abs(comparacion['diferencias']['od_esfera']),
            abs(comparacion['diferencias']['od_cilindro']),
            abs(comparacion['diferencias']['os_esfera']),
            abs(comparacion['diferencias']['os_cilindro'])
        )
        
        if max_diferencia >= 1.0:
            comparacion['analisis']['cambio_significativo'] = True
            comparacion['analisis']['recomendaciones'].append(
                f"Cambio significativo de {max_diferencia:.2f} dioptrías detectado"
            )
        
        if comparacion['diferencias']['meses_transcurridos'] < 12 and max_diferencia >= 0.5:
            comparacion['analisis']['recomendaciones'].append(
                "Cambio rápido en la graduación - considerar evaluación adicional"
            )
        
        return Response(comparacion)
    
    @action(detail=True, methods=['get'])
    def historial_cambios(self, request, pk=None):
        """Obtener historial de cambios de una prescripción"""
        prescripcion = self.get_object()
        cambios = HistorialCambios.objects.filter(
            prescripcion=prescripcion
        ).select_related('usuario').order_by('-fecha_cambio')
        
        serializer = HistorialCambiosSerializer(cambios, many=True)
        return Response({
            'prescripcion': prescripcion.numero_prescripcion,
            'total_cambios': cambios.count(),
            'cambios': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Estadísticas generales de prescripciones"""
        total_prescripciones = Prescripcion.objects.count()
        vigentes = Prescripcion.objects.filter(vigente=True).count()
        
        # Por vencer en 90 días
        fecha_limite = date.today() - timedelta(days=640)
        por_vencer = Prescripcion.objects.filter(
            vigente=True,
            fecha_examen__lte=fecha_limite
        ).count()
        
        # Con astigmatismo
        con_astigmatismo = Prescripcion.objects.filter(
            Q(od_cilindro__gt=0) | Q(od_cilindro__lt=0) |
            Q(os_cilindro__gt=0) | Q(os_cilindro__lt=0)
        ).count()
        
        # Con presbicia
        con_presbicia = Prescripcion.objects.filter(adicion__gt=0).count()
        
        # Por profesional (top 5)
        from django.db.models import Count
        por_profesional = Prescripcion.objects.values(
            'profesional__first_name', 'profesional__last_name'
        ).annotate(
            total=Count('id')
        ).order_by('-total')[:5]
        
        return Response({
            'resumen': {
                'total_prescripciones': total_prescripciones,
                'vigentes': vigentes,
                'por_vencer_90_dias': por_vencer,
                'porcentaje_vigentes': round((vigentes / total_prescripciones * 100) if total_prescripciones > 0 else 0, 2)
            },
            'caracteristicas': {
                'con_astigmatismo': con_astigmatismo,
                'con_presbicia': con_presbicia,
                'porcentaje_astigmatismo': round((con_astigmatismo / total_prescripciones * 100) if total_prescripciones > 0 else 0, 2),
                'porcentaje_presbicia': round((con_presbicia / total_prescripciones * 100) if total_prescripciones > 0 else 0, 2)
            },
            'por_profesional': por_profesional
        })


class HistorialCambiosViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para el historial de cambios
    """
    queryset = HistorialCambios.objects.all()
    serializer_class = HistorialCambiosSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['prescripcion', 'usuario', 'campo_modificado']
    ordering = ['-fecha_cambio']