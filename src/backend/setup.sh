#!/bin/bash

# Script de configuración automática para Óptica Visual Km 30
# Sigue las especificaciones del README.md y documentación técnica

echo "🚀 Configurando Sistema de Gestión Óptica Visual Km 30"
echo "======================================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con colores
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    print_error "Este script debe ejecutarse desde el directorio src/backend/"
    exit 1
fi

print_info "Verificando prerrequisitos del sistema..."

# Verificar PostgreSQL
if ! command -v psql &> /dev/null; then
    print_error "PostgreSQL no está instalado. Ejecute: sudo apt install postgresql postgresql-contrib"
    exit 1
fi
print_success "PostgreSQL encontrado"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no está instalado"
    exit 1
fi
print_success "Python 3 encontrado"

# Crear base de datos si no existe
print_info "Configurando base de datos PostgreSQL..."
sudo -u postgres psql -c "CREATE DATABASE optica_visual_km30;" 2>/dev/null || print_warning "Base de datos ya existe"
sudo -u postgres psql -c "CREATE USER optica_user WITH PASSWORD 'optica2025';" 2>/dev/null || print_warning "Usuario ya existe"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE optica_visual_km30 TO optica_user;"
sudo -u postgres psql -c "ALTER DATABASE optica_visual_km30 OWNER TO optica_user;"
print_success "Base de datos PostgreSQL configurada"

# Verificar entorno virtual
if [ ! -d "../../.venv" ]; then
    print_info "Creando entorno virtual..."
    cd ../..
    python3 -m venv .venv
    cd src/backend
    print_success "Entorno virtual creado"
fi

# Activar entorno virtual y instalar dependencias
print_info "Instalando dependencias..."
source ../../.venv/bin/activate
pip install -r ../../requirements/development.txt
print_success "Dependencias instaladas"

# Configurar archivo .env
if [ ! -f ".env" ]; then
    print_info "Creando archivo .env..."
    cp ../../.env.example .env
    print_success "Archivo .env creado"
else
    print_warning "Archivo .env ya existe"
fi

# Ejecutar migraciones
print_info "Ejecutando migraciones..."
python manage.py migrate
print_success "Migraciones aplicadas"

# Crear superusuario si no existe
print_info "Configurando superusuario..."
python manage.py shell -c "
from django.contrib.auth.models import User
try:
    User.objects.get(username='admin')
    print('Superusuario admin ya existe')
except User.DoesNotExist:
    User.objects.create_superuser('admin', 'admin@opticavisualkm30.com', 'admin123')
    print('Superusuario admin creado (password: admin123)')
"

# Cargar datos de prueba
print_info "Cargando datos de prueba..."
python manage.py shell -c "
import os
from datetime import date
from apps.pacientes.models import Paciente

pacientes_prueba = [
    {'tipo_documento': 'CC', 'numero_documento': '12345678', 'nombres': 'Juan Carlos', 'apellidos': 'Pérez González', 'fecha_nacimiento': date(1990, 5, 15), 'telefono': '3001234567', 'email': 'juan.perez@email.com', 'direccion': 'Calle 123 #45-67, Bogotá'},
    {'tipo_documento': 'CC', 'numero_documento': '87654321', 'nombres': 'María Elena', 'apellidos': 'Rodríguez López', 'fecha_nacimiento': date(1985, 8, 22), 'telefono': '3009876543', 'email': 'maria.rodriguez@email.com', 'direccion': 'Carrera 45 #123-89, Bogotá'},
    {'tipo_documento': 'CC', 'numero_documento': '11223344', 'nombres': 'Carlos Alberto', 'apellidos': 'Sánchez Martín', 'fecha_nacimiento': date(1978, 12, 3), 'telefono': '3005556677', 'email': 'carlos.sanchez@email.com', 'direccion': 'Avenida 68 #34-12, Bogotá'}
]

for paciente_data in pacientes_prueba:
    paciente, created = Paciente.objects.get_or_create(numero_documento=paciente_data['numero_documento'], defaults=paciente_data)
    if created:
        print(f'Paciente creado: {paciente.nombre_completo}')

print(f'Total pacientes: {Paciente.objects.count()}')
"
print_success "Datos de prueba cargados"

echo ""
echo "🎉 ¡Configuración completada exitosamente!"
echo "==========================================="
echo ""
print_info "Para iniciar el servidor ejecute:"
echo "   python manage.py runserver 0.0.0.0:8000"
echo ""
print_info "URLs disponibles:"
echo "   • Admin Django: http://localhost:8000/admin/ (admin/admin123)"
echo "   • API Pacientes: http://localhost:8000/api/pacientes/"
echo ""
print_info "Base de datos: PostgreSQL (optica_visual_km30)"
print_success "Sistema listo para desarrollo según especificaciones técnicas"