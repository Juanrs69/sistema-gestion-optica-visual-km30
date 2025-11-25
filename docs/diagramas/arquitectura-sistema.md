# Arquitectura del Sistema - Óptica Visual Km 30

```mermaid
graph TB
    %% Capa de Presentación
    subgraph "🖥️ CAPA DE PRESENTACIÓN"
        subgraph "Frontend Web"
            ADMIN[🏢 Panel Admin<br/>React + TypeScript]
            VENDOR[👩‍💼 Panel Vendedor<br/>React + Material-UI]
            OPTO[👩‍⚕️ Panel Optómetra<br/>React Specialized]
        end
        
        subgraph "APIs Externas"
            MOBILE[📱 App Móvil<br/>React Native]
            POS[🖨️ Sistema POS<br/>Integración Hardware]
        end
    end

    %% Capa de Aplicación
    subgraph "⚙️ CAPA DE APLICACIÓN"
        subgraph "API Gateway"
            NGINX[🌐 Nginx<br/>Load Balancer + SSL]
            CORS[🔗 CORS Handler]
        end
        
        subgraph "Backend Services"
            AUTH[🔐 Autenticación<br/>JWT + Sessions]
            API[📡 Django REST API<br/>Business Logic]
            TASKS[⏰ Celery Tasks<br/>Background Jobs]
        end
    end

    %% Capa de Lógica de Negocio
    subgraph "🧠 LÓGICA DE NEGOCIO"
        subgraph "Módulos Core"
            PACIENTES[👥 Gestión Pacientes<br/>CRUD + Validaciones]
            PRESCRIPCIONES[👁️ Prescripciones<br/>Validación Médica]
            INVENTARIO[📦 Inventario<br/>Stock + Alertas]
            FACTURACION[💰 Facturación<br/>Cálculos + DIAN]
        end
        
        subgraph "Módulos Avanzados"
            CREDITOS[💳 Gestión Créditos<br/>Scoring + Cobranza]
            MARKETING[📧 Marketing<br/>Campañas + CRM]
            REPORTES[📊 Business Intelligence<br/>Analytics + KPIs]
            WORKFLOW[🔄 Órdenes Trabajo<br/>Estados + Tracking]
        end
    end

    %% Capa de Datos
    subgraph "💾 CAPA DE DATOS"
        subgraph "Base de Datos Principal"
            POSTGRES[(🐘 PostgreSQL 15+<br/>Datos Transaccionales)]
        end
        
        subgraph "Cache y Sesiones"
            REDIS[(⚡ Redis<br/>Cache + Sessions)]
        end
        
        subgraph "Archivos y Media"
            MEDIA[📁 Sistema Archivos<br/>Imágenes + Documentos]
            BACKUP[💿 Backup Automático<br/>Cron Jobs]
        end
    end

    %% Sistemas Externos
    subgraph "🌐 INTEGRACIONES EXTERNAS"
        subgraph "Facturación Electrónica"
            DIAN[🏛️ DIAN<br/>Facturación Electrónica]
            CUFE[📄 Validador CUFE<br/>Firmas Digitales]
        end
        
        subgraph "Pagos"
            PSE[🏦 PSE<br/>Pagos Electrónicos]
            TARJETAS[💳 Pasarela Tarjetas<br/>Wompi/PayU]
        end
        
        subgraph "Comunicaciones"
            EMAIL[📧 SMTP Server<br/>Gmail/SendGrid]
            SMS[📱 SMS Gateway<br/>Twilio/Local]
            WHATSAPP[💬 WhatsApp Business<br/>API Oficial]
        end
        
        subgraph "Proveedores"
            LABS[🔬 Laboratorios<br/>APIs Disponibilidad]
            ERP[📋 ERPs Proveedores<br/>Integración B2B]
        end
    end

    %% Infraestructura
    subgraph "☁️ INFRAESTRUCTURA"
        subgraph "Contenedores"
            DOCKER[🐳 Docker<br/>Containerización]
            COMPOSE[📋 Docker Compose<br/>Orquestación Local]
        end
        
        subgraph "Monitoreo"
            LOGS[📝 Centralized Logs<br/>ELK Stack]
            METRICS[📈 Métricas<br/>Prometheus + Grafana]
            HEALTH[❤️ Health Checks<br/>Uptime Monitoring]
        end
        
        subgraph "Seguridad"
            SSL[🔒 SSL/TLS<br/>Let's Encrypt]
            FIREWALL[🛡️ Firewall<br/>IP Filtering]
            VAULT[🔐 Secrets Management<br/>Env Variables]
        end
    end

    %% Conexiones principales
    ADMIN --> NGINX
    VENDOR --> NGINX
    OPTO --> NGINX
    MOBILE --> NGINX
    POS --> NGINX

    NGINX --> AUTH
    NGINX --> API
    
    AUTH --> REDIS
    API --> PACIENTES
    API --> PRESCRIPCIONES
    API --> INVENTARIO
    API --> FACTURACION
    API --> CREDITOS
    API --> MARKETING
    API --> REPORTES
    
    PACIENTES --> POSTGRES
    PRESCRIPCIONES --> POSTGRES
    INVENTARIO --> POSTGRES
    FACTURACION --> POSTGRES
    CREDITOS --> POSTGRES
    MARKETING --> POSTGRES
    REPORTES --> POSTGRES
    
    FACTURACION --> DIAN
    CREDITOS --> PSE
    CREDITOS --> TARJETAS
    MARKETING --> EMAIL
    MARKETING --> SMS
    MARKETING --> WHATSAPP
    
    INVENTARIO --> LABS
    REPORTES --> ERP
    
    TASKS --> REDIS
    TASKS --> EMAIL
    
    API --> MEDIA
    POSTGRES --> BACKUP

    %% Estilos
    classDef frontend fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef backend fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef database fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef external fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef infrastructure fill:#fce4ec,stroke:#c2185b,stroke-width:2px

    class ADMIN,VENDOR,OPTO,MOBILE,POS frontend
    class AUTH,API,TASKS,PACIENTES,PRESCRIPCIONES,INVENTARIO,FACTURACION,CREDITOS,MARKETING,REPORTES,WORKFLOW backend
    class POSTGRES,REDIS,MEDIA,BACKUP database
    class DIAN,CUFE,PSE,TARJETAS,EMAIL,SMS,WHATSAPP,LABS,ERP external
    class DOCKER,COMPOSE,LOGS,METRICS,HEALTH,SSL,FIREWALL,VAULT infrastructure
```

## 📋 Especificaciones Técnicas por Capa

### 🖥️ **CAPA DE PRESENTACIÓN**

#### **Frontend Web (React 18+)**
- **Panel Administrador**: Gestión completa, reportes ejecutivos, configuraciones
- **Panel Vendedor**: Ventas, facturación, consulta inventario, créditos
- **Panel Optómetra**: Prescripciones, historiales médicos, órdenes trabajo
- **Tecnologías**: React + TypeScript + Material-UI + Redux Toolkit

#### **Aplicaciones Especializadas**
- **App Móvil**: React Native para inventario móvil y ventas externas
- **Sistema POS**: Integración con impresoras, lectores código barras, cajón

### ⚙️ **CAPA DE APLICACIÓN**

#### **API Gateway (Nginx)**
```nginx
# Configuración ejemplo
upstream backend {
    server django:8000;
}

server {
    listen 443 ssl;
    server_name opticavisualkm30.com;
    
    ssl_certificate /etc/letsencrypt/live/domain/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/domain/privkey.pem;
    
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /app/staticfiles/;
        expires 30d;
    }
}
```

#### **Backend Services (Django)**
- **Autenticación**: JWT + Session-based + 2FA
- **API REST**: DRF + Paginación + Filtrado + Serialización
- **Tasks Background**: Celery + Redis para emails, reportes, alertas

### 🧠 **LÓGICA DE NEGOCIO**

#### **Módulos Core**
```python
# Estructura modular
apps/
├── authentication/     # JWT + Permisos
├── pacientes/         # ✅ Implementado
├── prescripciones/    # ⏳ Siguiente
├── inventario/        # ⏳ Pendiente
├── facturacion/       # ⏳ Pendiente
├── creditos/          # ⏳ Pendiente
├── marketing/         # ⏳ Pendiente
├── reportes/          # ⏳ Pendiente
└── core/              # Utilidades comunes
```

### 💾 **CAPA DE DATOS**

#### **PostgreSQL (Principal)**
- **Versión**: 15+ con extensiones JSON y Full-Text Search
- **Configuraciones**: Connection pooling, índices optimizados
- **Backup**: pg_dump automático cada 6 horas + WAL archiving

#### **Redis (Cache + Sessions)**
```python
# Configuración Django
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Celery broker
CELERY_BROKER_URL = 'redis://redis:6379/0'
```

### 🌐 **INTEGRACIONES EXTERNAS**

#### **Facturación Electrónica DIAN**
```python
class FacturacionDIAN:
    def generar_factura_electronica(self, factura):
        # 1. Validar datos obligatorios
        # 2. Generar XML según estándar UBL 2.1
        # 3. Firmar digitalmente
        # 4. Enviar a DIAN
        # 5. Obtener CUFE
        # 6. Almacenar respuesta
        pass
```

#### **Pasarelas de Pago**
- **PSE**: Integración directa con bancos
- **Tarjetas**: Wompi, PayU, Mercado Pago
- **Wallets**: Nequi, Daviplata (futuro)

### ☁️ **INFRAESTRUCTURA**

#### **Docker Compose Completo**
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: optica_visual_km30
      POSTGRES_USER: optica_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
  redis:
    image: redis:7-alpine
    
  django:
    build: .
    depends_on:
      - postgres
      - redis
    environment:
      - DATABASE_URL=postgresql://optica_user:${DB_PASSWORD}@postgres:5432/optica_visual_km30
      
  celery:
    build: .
    command: celery -A optica_visual worker -l info
    depends_on:
      - postgres
      - redis
      
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - django
```

## 🔧 **Patrones de Arquitectura Implementados**

### **1. Clean Architecture**
- **Separación por capas**: Presentación → Aplicación → Dominio → Infraestructura
- **Inversión de dependencias**: Interfaces abstraen implementaciones
- **Independencia de frameworks**: Lógica de negocio aislada

### **2. Repository Pattern**
```python
class PacienteRepository:
    def get_by_documento(self, documento: str) -> Paciente:
        pass
    
    def search(self, criterios: dict) -> List[Paciente]:
        pass
```

### **3. Service Layer**
```python
class VentaService:
    def procesar_venta(self, venta_data: dict) -> Factura:
        # 1. Validar stock
        # 2. Calcular precios
        # 3. Aplicar descuentos
        # 4. Generar factura
        # 5. Actualizar inventario
        # 6. Procesar pago
        pass
```

### **4. Event-Driven Architecture**
```python
# Ejemplo: Al crear factura, disparar eventos
@receiver(post_save, sender=Factura)
def factura_creada(sender, instance, created, **kwargs):
    if created:
        # Actualizar inventario
        # Enviar email
        # Generar orden trabajo (si tiene lentes)
        pass
```

Esta arquitectura garantiza **escalabilidad**, **mantenibilidad** y **extensibilidad** para el crecimiento futuro del negocio. 🚀