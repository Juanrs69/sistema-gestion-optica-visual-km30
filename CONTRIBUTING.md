# Sistema de Gestión Integral - Óptica Visual Km 30

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-blue)](https://postgresql.org)
[![React](https://img.shields.io/badge/React-18%2B-blue)](https://reactjs.org)

Sistema integral de gestión empresarial para digitalizar y optimizar todos los procesos de Óptica Visual Km 30.

## Características Principales

- **Gestión de Pacientes**: Registro completo con historiales médicos
- **Prescripciones Oftalmológicas**: Control de fórmulas y medidas
- **Sistema de Facturación**: Generación automática y control de pagos
- **Gestión de Inventario**: Control de stock y productos
- **Control de Créditos**: Seguimiento de cuentas por cobrar
- **Marketing Digital**: Herramientas de campañas y seguimiento
- **Reportería Avanzada**: Dashboard e informes gerenciales

## Tecnologías Utilizadas

### Backend
- Python 3.11+
- Django 4.2 + Django REST Framework
- PostgreSQL 15+
- Celery para tareas asíncronas

### Frontend
- React 18+ con TypeScript
- Material-UI para componentes
- Redux Toolkit para manejo de estado

### DevOps
- Docker para containerización
- Nginx como proxy reverso
- Git para control de versiones

## Estructura del Proyecto

```
optica-visual-km30/
├── docs/                  # Documentación técnica
├── src/
│   ├── backend/          # API REST con Django
│   ├── frontend/         # Aplicación React
│   └── database/         # Scripts y migraciones
├── tests/                # Pruebas automatizadas
├── deployment/           # Configuración de despliegue
└── requirements/         # Dependencias Python
```

## Instalación Rápida

### Prerrequisitos
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Git

### Configuración del Proyecto

1. **Clonar el repositorio**
```bash
git clone https://github.com/tuusuario/optica-visual-km30.git
cd optica-visual-km30
```

2. **Setup Automático (Recomendado)**
```bash
cd src/backend
chmod +x setup.sh
./setup.sh
```

3. **Setup Manual (si prefieres control total)**
```bash
# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib libpq-dev

# Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements/development.txt

# Configurar PostgreSQL
sudo -u postgres psql -c "CREATE DATABASE optica_visual_km30;"
sudo -u postgres psql -c "CREATE USER optica_user WITH PASSWORD 'optica2025';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE optica_visual_km30 TO optica_user;"

# Configurar variables de entorno
cd src/backend
cp ../../.env.example .env
# Editar .env con DATABASE_URL=postgresql://optica_user:optica2025@localhost:5432/optica_visual_km30

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

4. **Iniciar Servidor de Desarrollo**
```bash
cd src/backend
python manage.py runserver 0.0.0.0:8000
```

### URLs Disponibles después del setup
- **Admin Django**: http://localhost:8000/admin/ (admin/admin123)
- **API Pacientes**: http://localhost:8000/api/pacientes/
- **API Root**: http://localhost:8000/api/

### Configuración Frontend (Próximamente)
```bash
cd src/frontend
npm install
npm run dev
```

## Documentación

- [Especificación Técnica](docs/especificacion-tecnica.md)
- [Manual de Instalación](docs/instalacion.md)
- [Diagramas UML](docs/diagramas/)
- [API Documentation](docs/api.md)

## Contribuciones

Este proyecto está siendo desarrollado por:
- **Juana** - Product Owner & Frontend Developer
- **Equipo Técnico** - Backend & Architecture

## Estado del Proyecto

🚧 **En Desarrollo Activo**

### Progreso Actual
- [x] Análisis y documentación inicial
- [x] Arquitectura del sistema
- [ ] Desarrollo del backend
- [ ] Desarrollo del frontend
- [ ] Testing e integración
- [ ] Deployment

## Licencia

Proyecto privado para Óptica Visual Km 30.

## Contacto

- **Empresa**: Óptica Visual Km 30
- **Ubicación**: Km 30 Vía Principal
- **Teléfono**: 300-123-4567