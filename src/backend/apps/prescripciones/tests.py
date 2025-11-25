from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from decimal import Decimal
from .models import Prescripcion, HistorialCambios
from apps.pacientes.models import Paciente


class PrescripcionModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Prescripcion
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear usuario profesional
        self.profesional = User.objects.create_user(
            username='optometra1',
            email='optometra@opticakm30.com',
            first_name='Dr. Juan',
            last_name='Pérez'
        )
        
        # Crear paciente
        self.paciente = Paciente.objects.create(
            tipo_documento='CC',
            numero_documento='12345678',
            nombres='María Elena',
            apellidos='González López',
            fecha_nacimiento=date(1980, 5, 15),
            telefono='3001234567',
            email='maria@email.com'
        )
        
        # Datos de prescripción válida
        self.prescripcion_data = {
            'paciente': self.paciente,
            'profesional': self.profesional,
            'fecha_examen': date.today(),
            'od_esfera': Decimal('-2.50'),
            'od_cilindro': Decimal('-1.25'),
            'od_eje': 90,
            'os_esfera': Decimal('-2.75'),
            'os_cilindro': Decimal('-1.00'),
            'os_eje': 85,
            'adicion': Decimal('1.50'),
            'distancia_pupilar': 62,
            'agudeza_visual_od': '20/20',
            'agudeza_visual_os': '20/25'
        }
    
    def test_crear_prescripcion_valida(self):
        """Prueba la creación de una prescripción con datos válidos"""
        prescripcion = Prescripcion.objects.create(**self.prescripcion_data)
        
        self.assertIsNotNone(prescripcion.numero_prescripcion)
        self.assertTrue(prescripcion.numero_prescripcion.startswith('PRES-'))
        self.assertTrue(prescripcion.vigente)
        self.assertEqual(prescripcion.paciente, self.paciente)
        self.assertEqual(prescripcion.profesional, self.profesional)
    
    def test_numero_prescripcion_unico(self):
        """Prueba que el número de prescripción sea único"""
        prescripcion1 = Prescripcion.objects.create(**self.prescripcion_data)
        
        # Crear segunda prescripción con datos diferentes
        self.prescripcion_data['od_esfera'] = Decimal('-3.00')
        prescripcion2 = Prescripcion.objects.create(**self.prescripcion_data)
        
        self.assertNotEqual(prescripcion1.numero_prescripcion, prescripcion2.numero_prescripcion)
    
    def test_validacion_rango_esfera(self):
        """Prueba la validación del rango de esfera"""
        # Valor fuera de rango
        self.prescripcion_data['od_esfera'] = Decimal('25.00')
        
        with self.assertRaises(ValidationError):
            prescripcion = Prescripcion(**self.prescripcion_data)
            prescripcion.full_clean()
    
    def test_validacion_rango_cilindro(self):
        """Prueba la validación del rango de cilindro"""
        self.prescripcion_data['od_cilindro'] = Decimal('8.00')
        
        with self.assertRaises(ValidationError):
            prescripcion = Prescripcion(**self.prescripcion_data)
            prescripcion.full_clean()
    
    def test_validacion_rango_eje(self):
        """Prueba la validación del rango de eje"""
        self.prescripcion_data['od_eje'] = 200
        
        with self.assertRaises(ValidationError):
            prescripcion = Prescripcion(**self.prescripcion_data)
            prescripcion.full_clean()
    
    def test_edad_paciente_en_examen(self):
        """Prueba el cálculo de edad del paciente al momento del examen"""
        prescripcion = Prescripcion.objects.create(**self.prescripcion_data)
        
        # El paciente nació en 1980, examen en fecha actual
        edad_esperada = date.today().year - 1980
        if (date.today().month, date.today().day) < (5, 15):  # Antes del cumpleaños
            edad_esperada -= 1
        
        self.assertEqual(prescripcion.edad_paciente_en_examen, edad_esperada)
    
    def test_propiedad_es_vigente(self):
        """Prueba la propiedad es_vigente"""
        # Prescripción actual
        prescripcion_actual = Prescripcion.objects.create(**self.prescripcion_data)
        self.assertTrue(prescripcion_actual.es_vigente)
        
        # Prescripción de hace 3 años (vencida)
        self.prescripcion_data['fecha_examen'] = date.today() - timedelta(days=1095)
        prescripcion_vencida = Prescripcion.objects.create(**self.prescripcion_data)
        self.assertFalse(prescripcion_vencida.es_vigente)
    
    def test_propiedad_tiene_astigmatismo(self):
        """Prueba la detección de astigmatismo"""
        prescripcion = Prescripcion.objects.create(**self.prescripcion_data)
        self.assertTrue(prescripcion.tiene_astigmatismo)
        
        # Sin astigmatismo
        self.prescripcion_data['od_cilindro'] = Decimal('0.00')
        self.prescripcion_data['os_cilindro'] = Decimal('0.00')
        prescripcion_sin_astigmatismo = Prescripcion.objects.create(**self.prescripcion_data)
        self.assertFalse(prescripcion_sin_astigmatismo.tiene_astigmatismo)
    
    def test_propiedad_tiene_presbicia(self):
        """Prueba la detección de presbicia"""
        prescripcion = Prescripcion.objects.create(**self.prescripcion_data)
        self.assertTrue(prescripcion.tiene_presbicia)
        
        # Sin presbicia
        self.prescripcion_data['adicion'] = None
        prescripcion_sin_presbicia = Prescripcion.objects.create(**self.prescripcion_data)
        self.assertFalse(prescripcion_sin_presbicia.tiene_presbicia)
    
    def test_graduacion_completa_formato(self):
        """Prueba el formato de graduación completa"""
        prescripcion = Prescripcion.objects.create(**self.prescripcion_data)
        
        graduacion_od = prescripcion.graduacion_od_completa
        self.assertIn('Esf: -2.50', graduacion_od)
        self.assertIn('Cil: -1.25', graduacion_od)
        self.assertIn('Eje: 90°', graduacion_od)
        self.assertIn('Add: +1.50', graduacion_od)
    
    def test_invalidar_prescripciones_anteriores(self):
        """Prueba que se invaliden prescripciones anteriores del mismo paciente"""
        # Crear primera prescripción
        prescripcion1 = Prescripcion.objects.create(**self.prescripcion_data)
        self.assertTrue(prescripcion1.vigente)
        
        # Crear segunda prescripción
        self.prescripcion_data['fecha_examen'] = date.today() + timedelta(days=30)
        self.prescripcion_data['od_esfera'] = Decimal('-3.00')
        prescripcion2 = Prescripcion.objects.create(**self.prescripcion_data)
        prescripcion2.invalidar_prescripciones_anteriores()
        
        # Verificar que la primera se haya invalidado
        prescripcion1.refresh_from_db()
        self.assertFalse(prescripcion1.vigente)
        self.assertTrue(prescripcion2.vigente)
    
    def test_calcular_diferencia_con_anterior(self):
        """Prueba el cálculo de diferencia con prescripción anterior"""
        # Crear primera prescripción
        prescripcion1 = Prescripcion.objects.create(**self.prescripcion_data)
        
        # Crear segunda prescripción con cambios
        self.prescripcion_data['fecha_examen'] = date.today() + timedelta(days=365)
        self.prescripcion_data['od_esfera'] = Decimal('-3.50')  # Cambio de 1.00 dioptría
        prescripcion2 = Prescripcion.objects.create(**self.prescripcion_data)
        
        diferencia = prescripcion2.calcular_diferencia_con_anterior()
        
        self.assertIsNotNone(diferencia)
        self.assertEqual(diferencia['od_esfera'], 1.00)
        self.assertEqual(diferencia['meses_transcurridos'], 12)
    
    def test_str_representation(self):
        """Prueba la representación en string del modelo"""
        prescripcion = Prescripcion.objects.create(**self.prescripcion_data)
        
        str_repr = str(prescripcion)
        self.assertIn(prescripcion.numero_prescripcion, str_repr)
        self.assertIn(self.paciente.nombre_completo, str_repr)
        self.assertIn(str(prescripcion.fecha_examen), str_repr)


class HistorialCambiosTest(TestCase):
    """
    Pruebas para el modelo HistorialCambios
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.profesional = User.objects.create_user(
            username='optometra1',
            first_name='Dr. Juan',
            last_name='Pérez'
        )
        
        self.paciente = Paciente.objects.create(
            numero_documento='12345678',
            nombres='Test',
            apellidos='Paciente',
            fecha_nacimiento=date(1980, 1, 1)
        )
        
        self.prescripcion = Prescripcion.objects.create(
            paciente=self.paciente,
            profesional=self.profesional,
            fecha_examen=date.today(),
            od_esfera=Decimal('-2.00'),
            os_esfera=Decimal('-2.00')
        )
    
    def test_crear_historial_cambio(self):
        """Prueba la creación de un registro de historial"""
        cambio = HistorialCambios.objects.create(
            prescripcion=self.prescripcion,
            campo_modificado='od_esfera',
            valor_anterior='-2.00',
            valor_nuevo='-2.50',
            usuario=self.profesional,
            motivo='Corrección tras nuevo examen'
        )
        
        self.assertEqual(cambio.prescripcion, self.prescripcion)
        self.assertEqual(cambio.campo_modificado, 'od_esfera')
        self.assertEqual(cambio.usuario, self.profesional)
        self.assertIsNotNone(cambio.fecha_cambio)