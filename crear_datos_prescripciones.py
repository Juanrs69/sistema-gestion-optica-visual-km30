"""
Script para crear datos de ejemplo de prescripciones
"""
import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Configurar Django
sys.path.append('/home/juana/proyectos/sistema-gestion-optica-visual-km30/src/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optica_visual.settings.base')
django.setup()

from django.contrib.auth.models import User
from apps.pacientes.models import Paciente
from apps.prescripciones.models import Prescripcion

def crear_datos_ejemplo():
    """Crea datos de ejemplo para pruebas"""
    
    # Crear o obtener profesional
    profesional, created = User.objects.get_or_create(
        username='optometra_km30',
        defaults={
            'first_name': 'Dr. Carlos',
            'last_name': 'Martínez',
            'email': 'carlos.martinez@opticakm30.com',
            'is_staff': True
        }
    )
    if created:
        profesional.set_password('admin123')
        profesional.save()
        print(f"✅ Profesional creado: {profesional.get_full_name()}")
    else:
        print(f"ℹ️ Profesional ya existe: {profesional.get_full_name()}")
    
    # Crear o obtener pacientes
    pacientes_data = [
        {
            'numero_documento': '12345678',
            'nombres': 'María Elena',
            'apellidos': 'González López',
            'fecha_nacimiento': date(1985, 3, 15),
            'telefono': '3001234567',
            'email': 'maria.gonzalez@email.com'
        },
        {
            'numero_documento': '87654321',
            'nombres': 'José Antonio',
            'apellidos': 'Rodríguez Pérez',
            'fecha_nacimiento': date(1978, 11, 22),
            'telefono': '3109876543',
            'email': 'jose.rodriguez@email.com'
        },
        {
            'numero_documento': '11223344',
            'nombres': 'Ana Lucía',
            'apellidos': 'Mendoza Silva',
            'fecha_nacimiento': date(1992, 7, 8),
            'telefono': '3158765432',
            'email': 'ana.mendoza@email.com'
        }
    ]
    
    pacientes = []
    for data in pacientes_data:
        paciente, created = Paciente.objects.get_or_create(
            numero_documento=data['numero_documento'],
            defaults=data
        )
        pacientes.append(paciente)
        if created:
            print(f"✅ Paciente creado: {paciente.nombre_completo}")
        else:
            print(f"ℹ️ Paciente ya existe: {paciente.nombre_completo}")
    
    # Crear prescripciones de ejemplo
    prescripciones_data = [
        {
            'paciente': pacientes[0],  # María Elena
            'profesional': profesional,
            'fecha_examen': date.today() - timedelta(days=30),
            'od_esfera': Decimal('-2.50'),
            'od_cilindro': Decimal('-1.25'),
            'od_eje': 90,
            'os_esfera': Decimal('-2.75'),
            'os_cilindro': Decimal('-1.00'),
            'os_eje': 85,
            'adicion': Decimal('1.50'),
            'distancia_pupilar': 62,
            'agudeza_visual_od': '20/20',
            'agudeza_visual_os': '20/25',
            'observaciones': 'Paciente refiere fatiga visual al final del día. Se recomienda uso continuo de lentes.'
        },
        {
            'paciente': pacientes[1],  # José Antonio
            'profesional': profesional,
            'fecha_examen': date.today() - timedelta(days=15),
            'od_esfera': Decimal('1.00'),
            'od_cilindro': Decimal('-0.50'),
            'od_eje': 180,
            'os_esfera': Decimal('1.25'),
            'os_cilindro': Decimal('-0.75'),
            'os_eje': 175,
            'adicion': Decimal('2.00'),
            'distancia_pupilar': 65,
            'agudeza_visual_od': '20/30',
            'agudeza_visual_os': '20/30',
            'observaciones': 'Hipermetropía con presbicia. Paciente necesita lentes bifocales o progresivos.'
        },
        {
            'paciente': pacientes[2],  # Ana Lucía
            'profesional': profesional,
            'fecha_examen': date.today() - timedelta(days=7),
            'od_esfera': Decimal('-4.25'),
            'od_cilindro': Decimal('-2.50'),
            'od_eje': 45,
            'os_esfera': Decimal('-4.00'),
            'os_cilindro': Decimal('-2.25'),
            'os_eje': 50,
            'distancia_pupilar': 58,
            'agudeza_visual_od': '20/40',
            'agudeza_visual_os': '20/35',
            'observaciones': 'Miopía alta con astigmatismo significativo. Control anual recomendado.'
        },
        {
            'paciente': pacientes[0],  # María Elena - prescripción anterior
            'profesional': profesional,
            'fecha_examen': date.today() - timedelta(days=395),  # Hace más de 1 año
            'od_esfera': Decimal('-2.00'),
            'od_cilindro': Decimal('-1.00'),
            'od_eje': 85,
            'os_esfera': Decimal('-2.25'),
            'os_cilindro': Decimal('-0.75'),
            'os_eje': 80,
            'adicion': Decimal('1.25'),
            'distancia_pupilar': 62,
            'agudeza_visual_od': '20/25',
            'agudeza_visual_os': '20/30',
            'vigente': False,  # Prescripción anterior, ya no vigente
            'observaciones': 'Prescripción anterior. Progresión de la miopía detectada.'
        }
    ]
    
    for i, data in enumerate(prescripciones_data):
        # Verificar si ya existe una prescripción similar
        existe = Prescripcion.objects.filter(
            paciente=data['paciente'],
            fecha_examen=data['fecha_examen']
        ).exists()
        
        if not existe:
            prescripcion = Prescripcion.objects.create(**data)
            print(f"✅ Prescripción creada: {prescripcion.numero_prescripcion} para {prescripcion.paciente.nombre_completo}")
        else:
            print(f"ℹ️ Prescripción ya existe para {data['paciente'].nombre_completo} en fecha {data['fecha_examen']}")
    
    print(f"\n📊 Resumen:")
    print(f"• Profesionales: {User.objects.count()}")
    print(f"• Pacientes: {Paciente.objects.count()}")
    print(f"• Prescripciones totales: {Prescripcion.objects.count()}")
    print(f"• Prescripciones vigentes: {Prescripcion.objects.filter(vigente=True).count()}")
    
    # Mostrar endpoints disponibles
    print(f"\n🌐 Endpoints de API disponibles:")
    print(f"• GET /api/prescripciones/ - Listar todas las prescripciones")
    print(f"• POST /api/prescripciones/ - Crear nueva prescripción")
    print(f"• GET /api/prescripciones/vigentes/ - Prescripciones vigentes")
    print(f"• GET /api/prescripciones/por_vencer/ - Prescripciones próximas a vencer")
    print(f"• GET /api/prescripciones/estadisticas/ - Estadísticas generales")
    print(f"• GET /api/prescripciones/{{id}}/historial_paciente/ - Historial de un paciente")

if __name__ == '__main__':
    crear_datos_ejemplo()