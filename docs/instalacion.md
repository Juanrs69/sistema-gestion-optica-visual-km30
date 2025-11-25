# Manual de Instalación y Configuración

## Prerrequisitos del Sistema

### Software Requerido
- **Python**: 3.11 o superior
- **Node.js**: 18 o superior
- **PostgreSQL**: 15 o superior
- **Docker**: Opcional pero recomendado
- **Git**: Para control de versiones

### Configuración del Entorno de Desarrollo

#### 1. Clonar el Repositorio
```bash
git clone https://github.com/tuusuario/optica-visual-km30.git
cd optica-visual-km30
```

#### 2. Configurar Backend (Python/Django)
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements/development.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones
```

#### 3. Configurar Base de Datos PostgreSQL
```bash
# Instalar PostgreSQL (Ubuntu/Debian)
sudo apt install postgresql postgresql-contrib libpq-dev

# Crear base de datos y usuario
sudo -u postgres psql -c "CREATE DATABASE optica_visual_km30;"
sudo -u postgres psql -c "CREATE USER optica_user WITH PASSWORD 'optica2025';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE optica_visual_km30 TO optica_user;"
sudo -u postgres psql -c "ALTER DATABASE optica_visual_km30 OWNER TO optica_user;"

# Ejecutar migraciones
cd src/backend
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

#### 3.1. Setup Automático (Recomendado)
```bash
# Ejecutar script de configuración automática
cd src/backend
chmod +x setup.sh
./setup.sh
```

#### 4. Configurar Frontend (React)
```bash
cd frontend
npm install
npm run dev
```

## Configuración de Producción

### Docker Deployment
```yaml
# docker-compose.yml incluido en el proyecto
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: optica_visual_km30
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your_password
    
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
```

### Variables de Entorno Críticas
```env
# .env
SECRET_KEY=tu_clave_secreta_django
DEBUG=False
DATABASE_URL=postgresql://user:pass@localhost:5432/optica_visual_km30
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
```

## Comandos Útiles de Desarrollo

```bash
# Ejecutar servidor de desarrollo
python manage.py runserver

# Ejecutar tests
python manage.py test

# Crear nueva aplicación Django
python manage.py startapp nombre_app

# Generar requirements.txt
pip freeze > requirements.txt
```