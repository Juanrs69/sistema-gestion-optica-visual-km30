# Especificación Técnica del Sistema

## 1. Análisis de Requerimientos

### 1.1 Requerimientos Funcionales

#### RF001 - Gestión de Pacientes
- **Descripción**: El sistema debe permitir registrar, modificar, eliminar y consultar información de pacientes
- **Criterios de Aceptación**:
  - Registro completo de datos personales
  - Historial médico oftalmológico
  - Búsqueda por múltiples criterios
  - Validación de datos obligatorios

#### RF002 - Gestión de Prescripciones
- **Descripción**: Registro y control de fórmulas oftalmológicas
- **Criterios de Aceptación**:
  - Captura de medidas OD/OS
  - Registro de fecha y profesional
  - Historial de prescripciones por paciente
  - Generación de órdenes de trabajo

#### RF003 - Sistema de Facturación
- **Descripción**: Generación y control de facturas de venta
- **Criterios de Aceptación**:
  - Creación automática de facturas
  - Cálculo de impuestos
  - Múltiples formas de pago
  - Impresión y envío por email

#### RF004 - Gestión de Inventario
- **Descripción**: Control de productos y stock
- **Criterios de Aceptación**:
  - Registro de productos por categorías
  - Control de existencias en tiempo real
  - Alertas de stock mínimo
  - Gestión de proveedores

#### RF005 - Control de Créditos
- **Descripción**: Gestión de cuentas por cobrar
- **Criterios de Aceptación**:
  - Registro de créditos otorgados
  - Seguimiento de pagos
  - Notificaciones automáticas
  - Reportes de cartera

#### RF006 - Marketing Digital
- **Descripción**: Herramientas para campañas y seguimiento
- **Criterios de Aceptación**:
  - Base de datos de clientes
  - Envío de campañas por email/SMS
  - Seguimiento de cumpleaños
  - Análisis de efectividad

### 1.2 Requerimientos No Funcionales

#### RNF001 - Performance
- Tiempo de respuesta máximo: 2 segundos
- Soporte para 100 usuarios concurrentes
- Disponibilidad 99.5%

#### RNF002 - Seguridad
- Autenticación de usuarios
- Encriptación de datos sensibles
- Backup automático diario
- Logs de auditoría

#### RNF003 - Usabilidad
- Interfaz intuitiva y responsive
- Soporte para dispositivos móviles
- Capacitación mínima requerida

#### RNF004 - Escalabilidad
- Arquitectura modular
- Base de datos escalable
- Posibilidad de integración con otros sistemas

## 2. Arquitectura del Sistema

### 2.1 Patrón Arquitectónico
**Modelo**: Arquitectura de 3 capas con patrón MVC

```
┌─────────────────┐
│   Presentación  │  ← Frontend (React/Vue.js)
├─────────────────┤
│     Lógica      │  ← Backend (Python Django/FastAPI)
├─────────────────┤
│      Datos      │  ← Base de Datos (PostgreSQL)
└─────────────────┘
```

### 2.2 Stack Tecnológico

#### Backend
- **Lenguaje**: Python 3.11+
- **Framework**: Django 4.2 con Django REST Framework
- **Base de Datos**: PostgreSQL 15+
- **ORM**: Django ORM
- **Autenticación**: Django Authentication + JWT

#### Frontend
- **Framework**: React 18+ con TypeScript
- **Estado**: Redux Toolkit
- **UI Components**: Material-UI
- **HTTP Client**: Axios
- **Build Tool**: Vite

#### Infraestructura
- **Containerización**: Docker + Docker Compose
- **Servidor Web**: Nginx
- **Base de Datos**: PostgreSQL en contenedor
- **Monitoreo**: Logs centralizados

### 2.3 Diagrama de Arquitectura

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Cliente   │◄──►│   Nginx     │◄──►│   Django    │
│  (Browser)  │    │ (Proxy/LB)  │    │   Backend   │
└─────────────┘    └─────────────┘    └─────────────┘
                                              │
                                              ▼
                                    ┌─────────────┐
                                    │ PostgreSQL  │
                                    │  Database   │
                                    └─────────────┘
```

## 3. Modelo de Base de Datos

### 3.1 Entidades Principales

#### Pacientes
```sql
- id (PK)
- numero_documento
- tipo_documento
- nombres
- apellidos
- fecha_nacimiento
- telefono
- email
- direccion
- fecha_registro
```

#### Prescripciones
```sql
- id (PK)
- paciente_id (FK)
- fecha_examen
- profesional
- od_esfera, od_cilindro, od_eje
- os_esfera, os_cilindro, os_eje
- adicion
- observaciones
```

#### Productos
```sql
- id (PK)
- codigo
- nombre
- categoria
- marca
- precio_compra
- precio_venta
- stock_actual
- stock_minimo
```

#### Facturas
```sql
- id (PK)
- numero_factura
- paciente_id (FK)
- fecha
- subtotal
- impuestos
- total
- estado
- forma_pago
```

### 3.2 Relaciones
- Un paciente puede tener múltiples prescripciones
- Una factura pertenece a un paciente
- Una factura puede tener múltiples productos (detalle_factura)
- Un crédito está asociado a una factura

## 4. Casos de Uso

### CU001 - Registrar Nuevo Paciente
**Actor**: Empleado
**Precondición**: Usuario autenticado
**Flujo Principal**:
1. Usuario selecciona "Nuevo Paciente"
2. Sistema muestra formulario
3. Usuario ingresa datos obligatorios
4. Sistema valida información
5. Sistema guarda paciente
6. Sistema confirma registro

### CU002 - Generar Factura
**Actor**: Empleado
**Precondición**: Paciente registrado, productos en inventario
**Flujo Principal**:
1. Usuario selecciona paciente
2. Usuario agrega productos
3. Sistema calcula totales
4. Usuario confirma venta
5. Sistema genera factura
6. Sistema actualiza inventario

### CU003 - Consultar Cartera de Créditos
**Actor**: Administrador
**Precondición**: Usuario con permisos administrativos
**Flujo Principal**:
1. Usuario accede a módulo de créditos
2. Sistema muestra lista de créditos
3. Usuario puede filtrar por estado/fecha
4. Sistema genera reporte

## 5. Estimación de Esfuerzo

### Módulos de Desarrollo
1. **Setup Inicial y Base**: 40 horas
2. **Gestión de Pacientes**: 60 horas
3. **Sistema de Facturación**: 80 horas
4. **Gestión de Inventario**: 70 horas
5. **Control de Créditos**: 50 horas
6. **Marketing**: 60 horas
7. **Frontend Completo**: 120 horas
8. **Testing e Integración**: 40 horas

**Total Estimado**: 520 horas de desarrollo