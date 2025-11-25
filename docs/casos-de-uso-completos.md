# Casos de Uso Completos - Sistema Óptica Visual Km 30

## 1. ACTORES DEL SISTEMA

### Actores Primarios
- **Administrador**: Gestión completa del sistema, reportes, configuraciones
- **Vendedor**: Atención al cliente, facturación, gestión básica de inventario
- **Técnico Optómetra**: Exámenes visuales, prescripciones, historiales médicos
- **Cliente/Paciente**: Consulta de historiales, citas (futuro módulo web)

### Actores Secundarios
- **Sistema de Facturación DIAN**: Validación de facturas electrónicas
- **Pasarela de Pagos**: Procesamiento de pagos con tarjeta
- **Proveedor**: Consulta de disponibilidad de productos (API externa)

---

## 2. CASOS DE USO POR MÓDULO

### 📋 MÓDULO: GESTIÓN DE PACIENTES

#### CU-PAC-001: Registrar Paciente
**Actor Principal**: Vendedor, Técnico Optómetra
**Descripción**: Registrar un nuevo paciente en el sistema
**Precondiciones**: Usuario autenticado con permisos de registro
**Postcondiciones**: Paciente registrado con número único

**Flujo Principal**:
1. Usuario selecciona "Nuevo Paciente"
2. Sistema muestra formulario de registro
3. Usuario ingresa datos obligatorios (documento, nombres, apellidos, fecha nacimiento)
4. Usuario ingresa datos opcionales (teléfono, email, dirección)
5. Sistema valida formato de datos
6. Sistema verifica unicidad del número de documento
7. Sistema guarda el paciente
8. Sistema genera número de paciente automático
9. Sistema muestra confirmación con datos del paciente

**Flujos Alternativos**:
- 6a. Número de documento ya existe
  - 6a.1. Sistema muestra mensaje de error
  - 6a.2. Sistema sugiere buscar paciente existente
  - 6a.3. Retorna al paso 3
- 5a. Datos inválidos
  - 5a.1. Sistema resalta campos con errores
  - 5a.2. Sistema muestra mensajes específicos
  - 5a.3. Retorna al paso 3

**Casos Especiales**:
- Paciente menor de edad (requiere datos del acudiente)
- Documento extranjero (validaciones diferentes)

#### CU-PAC-002: Buscar Paciente
**Actor Principal**: Vendedor, Técnico Optómetra, Administrador
**Descripción**: Buscar pacientes existentes por múltiples criterios

**Flujo Principal**:
1. Usuario accede al módulo de búsqueda
2. Sistema muestra opciones de búsqueda
3. Usuario ingresa criterio (documento, nombre, teléfono, email)
4. Sistema ejecuta búsqueda en tiempo real
5. Sistema muestra resultados ordenados por relevancia
6. Usuario selecciona paciente de la lista
7. Sistema muestra perfil completo del paciente

#### CU-PAC-003: Actualizar Información de Paciente
**Actor Principal**: Vendedor, Técnico Optómetra
**Descripción**: Modificar datos existentes de un paciente

**Flujo Principal**:
1. Usuario busca y selecciona paciente
2. Sistema muestra datos actuales en formulario editable
3. Usuario modifica campos necesarios
4. Sistema valida cambios
5. Sistema solicita confirmación
6. Usuario confirma cambios
7. Sistema registra modificación con timestamp y usuario
8. Sistema muestra confirmación

#### CU-PAC-004: Desactivar Paciente
**Actor Principal**: Administrador
**Descripción**: Desactivar paciente sin eliminar historial

---

### 👁️ MÓDULO: GESTIÓN DE PRESCRIPCIONES

#### CU-PRES-001: Crear Prescripción Oftalmológica
**Actor Principal**: Técnico Optómetra
**Descripción**: Registrar nueva fórmula visual para un paciente

**Flujo Principal**:
1. Usuario busca y selecciona paciente
2. Sistema muestra historial de prescripciones previas
3. Usuario selecciona "Nueva Prescripción"
4. Sistema muestra formulario de examen visual
5. Usuario ingresa medidas del ojo derecho (OD):
   - Esfera (-20.00 a +20.00)
   - Cilindro (-6.00 a +6.00) 
   - Eje (0° a 180°)
6. Usuario ingresa medidas del ojo izquierdo (OS)
7. Usuario ingresa adición para presbicia (si aplica)
8. Usuario ingresa distancia pupilar
9. Usuario agrega observaciones médicas
10. Sistema calcula automáticamente diferencias con prescripción anterior
11. Usuario guarda prescripción
12. Sistema genera código único de prescripción
13. Sistema actualiza historial del paciente

#### CU-PRES-002: Consultar Historial de Prescripciones
**Actor Principal**: Técnico Optómetra, Vendedor
**Descripción**: Ver evolución de la vista del paciente

#### CU-PRES-003: Generar Orden de Trabajo
**Actor Principal**: Vendedor, Técnico Optómetra
**Descripción**: Crear orden de manufactura basada en prescripción

---

### 📦 MÓDULO: GESTIÓN DE INVENTARIO

#### CU-INV-001: Registrar Producto
**Actor Principal**: Administrador, Vendedor
**Descripción**: Agregar nuevo producto al catálogo

**Flujo Principal**:
1. Usuario selecciona "Nuevo Producto"
2. Sistema muestra formulario por categoría
3. Usuario selecciona categoría:
   - Monturas
   - Lentes oftálmicos
   - Lentes de contacto
   - Lentes de sol
   - Accesorios
4. Sistema muestra campos específicos por categoría
5. Usuario ingresa información básica:
   - Código de producto
   - Nombre comercial
   - Marca
   - Modelo
6. Usuario ingresa información comercial:
   - Precio de compra
   - Precio de venta
   - Stock inicial
   - Stock mínimo
7. Usuario carga imágenes del producto
8. Sistema valida unicidad del código
9. Sistema guarda producto
10. Sistema genera código QR para inventario

#### CU-INV-002: Actualizar Stock
**Actor Principal**: Administrador, Vendedor
**Descripción**: Registrar entradas y salidas de inventario

#### CU-INV-003: Consultar Disponibilidad
**Actor Principal**: Vendedor
**Descripción**: Verificar stock disponible durante venta

#### CU-INV-004: Generar Alertas de Stock Mínimo
**Actor Principal**: Sistema (automático)
**Descripción**: Notificar cuando productos están por agotarse

---

### 💰 MÓDULO: FACTURACIÓN Y VENTAS

#### CU-FAC-001: Procesar Venta
**Actor Principal**: Vendedor
**Descripción**: Registrar venta completa con facturación

**Flujo Principal**:
1. Vendedor busca/selecciona paciente
2. Sistema muestra perfil del cliente
3. Vendedor selecciona "Nueva Venta"
4. Sistema muestra carrito de compras vacío
5. Vendedor agrega productos:
   5a. Busca producto por código/nombre
   5b. Verifica disponibilidad en stock
   5c. Agrega al carrito con cantidad
6. Si incluye lentes graduados:
   6a. Vendedor selecciona prescripción vigente
   6b. Sistema calcula precio según especificaciones
7. Sistema calcula subtotal
8. Sistema aplica descuentos (si aplican)
9. Sistema calcula impuestos (IVA)
10. Sistema muestra total final
11. Vendedor selecciona forma de pago:
    - Efectivo
    - Tarjeta débito/crédito
    - Transferencia
    - Crédito (cuotas)
12. Sistema procesa pago según método
13. Sistema genera factura electrónica
14. Sistema actualiza inventario
15. Sistema imprime factura
16. Sistema envía factura por email (opcional)

#### CU-FAC-002: Generar Factura Electrónica
**Actor Principal**: Sistema (automático)
**Descripción**: Crear factura válida ante DIAN

#### CU-FAC-003: Procesar Devolución
**Actor Principal**: Administrador, Vendedor Senior
**Descripción**: Gestionar devoluciones de productos

---

### 💳 MÓDULO: GESTIÓN DE CRÉDITOS

#### CU-CRED-001: Otorgar Crédito
**Actor Principal**: Administrador, Vendedor
**Descripción**: Aprobar venta a crédito con plan de pagos

**Flujo Principal**:
1. Durante proceso de venta, cliente solicita crédito
2. Vendedor selecciona "Pago a Crédito"
3. Sistema solicita información crediticia:
   - Ingresos mensuales
   - Referencias comerciales
   - Referencias familiares
4. Sistema evalúa historial de pagos previos del cliente
5. Vendedor/Sistema determina cupo de crédito
6. Sistema genera plan de pagos:
   - Número de cuotas
   - Valor de cuotas
   - Fechas de vencimiento
   - Intereses (si aplican)
7. Cliente acepta términos y condiciones
8. Sistema crea cuenta por cobrar
9. Sistema programa recordatorios automáticos
10. Sistema genera pagaré digital

#### CU-CRED-002: Registrar Pago de Cuota
**Actor Principal**: Vendedor
**Descripción**: Registrar abono a crédito existente

#### CU-CRED-003: Generar Recordatorios de Pago
**Actor Principal**: Sistema (automático)
**Descripción**: Enviar notificaciones antes del vencimiento

---

### 📈 MÓDULO: REPORTES Y ANÁLISIS

#### CU-REP-001: Generar Reporte de Ventas
**Actor Principal**: Administrador
**Descripción**: Crear informes de ventas por períodos

#### CU-REP-002: Dashboard Gerencial
**Actor Principal**: Administrador
**Descripción**: Vista ejecutiva con KPIs principales

---

### 📧 MÓDULO: MARKETING Y CRM

#### CU-MARK-001: Crear Campaña de Marketing
**Actor Principal**: Administrador
**Descripción**: Diseñar campaña dirigida a segmentos específicos

#### CU-MARK-002: Seguimiento de Cumpleaños
**Actor Principal**: Sistema (automático)
**Descripción**: Enviar felicitaciones y promociones

---

## 3. MATRIZ DE TRAZABILIDAD

| Caso de Uso | Requerimiento Funcional | Prioridad | Estado |
|-------------|-------------------------|-----------|---------|
| CU-PAC-001 | RF-001 | Alta | ✅ Implementado |
| CU-PAC-002 | RF-001 | Alta | ✅ Implementado |
| CU-PAC-003 | RF-001 | Alta | ✅ Implementado |
| CU-PRES-001 | RF-002 | Alta | ⏳ Pendiente |
| CU-INV-001 | RF-004 | Alta | ⏳ Pendiente |
| CU-FAC-001 | RF-003 | Alta | ⏳ Pendiente |

---

## 4. REGLAS DE NEGOCIO

### RN-001: Validación de Prescripciones
- Las prescripciones tienen vigencia de 2 años
- Solo optómetras registrados pueden crear prescripciones
- Cambios mayores a 1.00 dioptrías requieren confirmación

### RN-002: Gestión de Inventario
- Stock no puede ser negativo
- Alertas cuando stock < stock_mínimo
- Productos vencidos no se pueden vender

### RN-003: Políticas de Crédito
- Crédito máximo: 3 salarios mínimos
- Plazo máximo: 12 cuotas
- Interés moratorio: 1.5% mensual

### RN-004: Facturación
- Facturas > $100,000 requieren facturación electrónica
- Descuentos > 15% requieren autorización gerencial
- Devoluciones solo hasta 30 días después de compra