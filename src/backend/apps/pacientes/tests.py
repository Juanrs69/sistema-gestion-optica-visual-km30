from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import date, timedelta
from .models import Paciente


class PacienteModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Paciente
    """
    
    def setUp(self):
        """
        Configuración inicial para las pruebas
        """
        self.paciente_data = {
            'tipo_documento': 'CC',
            'numero_documento': '12345678',
            'nombres': 'Juan Carlos',
            'apellidos': 'Pérez González',
            'fecha_nacimiento': date(1990, 5, 15),
            'telefono': '3001234567',
            'email': 'juan.perez@email.com',
            'direccion': 'Calle 123 #45-67'
        }
    
    def test_crear_paciente_valido(self):
        """
        Prueba la creación de un paciente con datos válidos
        """
        paciente = Paciente.objects.create(**self.paciente_data)
        
        self.assertEqual(paciente.numero_documento, '12345678')
        self.assertEqual(paciente.nombres, 'Juan Carlos')
        self.assertEqual(paciente.apellidos, 'Pérez González')
        self.assertTrue(paciente.activo)
        self.assertIsNotNone(paciente.fecha_registro)
    
    def test_numero_documento_unico(self):
        """
        Prueba que el número de documento sea único
        """
        Paciente.objects.create(**self.paciente_data)
        
        # Intentar crear otro paciente con el mismo número de documento
        with self.assertRaises(IntegrityError):
            Paciente.objects.create(**self.paciente_data)
    
    def test_nombre_completo_property(self):
        """
        Prueba la propiedad nombre_completo
        """
        paciente = Paciente.objects.create(**self.paciente_data)
        
        expected_name = f"{self.paciente_data['nombres']} {self.paciente_data['apellidos']}"
        self.assertEqual(paciente.nombre_completo, expected_name)
    
    def test_edad_property(self):
        """
        Prueba el cálculo de edad
        """
        # Paciente de 30 años (aproximadamente)
        fecha_nacimiento = date.today() - timedelta(days=30*365)
        self.paciente_data['fecha_nacimiento'] = fecha_nacimiento
        
        paciente = Paciente.objects.create(**self.paciente_data)
        
        # La edad debería ser aproximadamente 30
        self.assertAlmostEqual(paciente.edad, 30, delta=1)
    
    def test_str_representation(self):
        """
        Prueba la representación en string del modelo
        """
        paciente = Paciente.objects.create(**self.paciente_data)
        
        expected_str = f"{paciente.nombres} {paciente.apellidos} - {paciente.numero_documento}"
        self.assertEqual(str(paciente), expected_str)
    
    def test_paciente_sin_campos_opcionales(self):
        """
        Prueba crear paciente sin campos opcionales
        """
        data_minima = {
            'tipo_documento': 'CC',
            'numero_documento': '87654321',
            'nombres': 'María',
            'apellidos': 'López',
            'fecha_nacimiento': date(1995, 8, 20),
        }
        
        paciente = Paciente.objects.create(**data_minima)
        
        self.assertEqual(paciente.telefono, '')
        self.assertEqual(paciente.email, '')
        self.assertEqual(paciente.direccion, '')
        self.assertTrue(paciente.activo)