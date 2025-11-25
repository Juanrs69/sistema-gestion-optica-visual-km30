# Diagrama de Secuencia - Sistema Óptica Visual Km 30

## Secuencia 1: Proceso Completo de Venta

```mermaid
sequenceDiagram
    participant V as Vendedor
    participant S as Sistema
    participant DB as Base de Datos
    participant INV as Módulo Inventario
    participant FAC as Módulo Facturación
    participant DIAN as Sistema DIAN
    participant PAY as Pasarela Pagos

    Note over V,PAY: Proceso Completo de Venta con Facturación

    V->>S: Iniciar nueva venta
    S->>V: Mostrar interfaz de venta

    V->>S: Buscar paciente (documento)
    S->>DB: Consultar paciente
    DB-->>S: Datos del paciente
    S->>V: Mostrar perfil del cliente

    V->>S: Agregar producto al carrito
    S->>INV: Verificar disponibilidad
    INV->>DB: Consultar stock
    DB-->>INV: Stock disponible: 5 unidades
    INV-->>S: Producto disponible
    S->>V: Confirmar producto agregado

    V->>S: Agregar lentes graduados
    S->>V: Solicitar prescripción
    V->>S: Seleccionar prescripción vigente
    S->>DB: Validar vigencia prescripción
    DB-->>S: Prescripción válida (6 meses)
    S->>V: Mostrar calculador de precio

    V->>S: Finalizar carrito
    S->>S: Calcular subtotal
    S->>S: Aplicar descuentos
    S->>S: Calcular IVA (19%)
    S->>V: Mostrar total: $850,000

    V->>S: Seleccionar forma pago: Tarjeta
    S->>PAY: Iniciar transacción ($850,000)
    PAY->>V: Solicitar datos tarjeta
    V->>PAY: Ingresar datos
    PAY-->>S: Pago autorizado (ID: TXN123456)

    S->>INV: Reducir stock productos
    INV->>DB: UPDATE stock
    DB-->>INV: Stock actualizado

    S->>FAC: Generar factura electrónica
    FAC->>DB: Crear registro factura
    DB-->>FAC: Factura #001234 creada
    FAC->>DIAN: Enviar factura electrónica
    DIAN-->>FAC: CUFE: ABC123XYZ789
    FAC-->>S: Factura validada

    S->>V: Mostrar confirmación venta
    S->>S: Imprimir factura
    S->>S: Enviar email al cliente

    Note over V,DIAN: Venta completada exitosamente
```

## Secuencia 2: Creación de Prescripción Oftalmológica

```mermaid
sequenceDiagram
    participant O as Optómetra
    participant S as Sistema
    participant DB as Base de Datos
    participant VAL as Validador
    participant NOT as Notificaciones

    Note over O,NOT: Proceso de Examen Visual y Prescripción

    O->>S: Buscar paciente para examen
    S->>DB: Consultar historial paciente
    DB-->>S: Paciente + prescripciones anteriores
    S->>O: Mostrar historial médico

    O->>S: Iniciar nueva prescripción
    S->>O: Formulario examen visual

    O->>S: Ingresar medidas OD (Esfera: -2.50)
    S->>VAL: Validar rango esfera (-20 a +20)
    VAL-->>S: Valor válido
    
    O->>S: Ingresar medidas OS (Cilindro: -1.25)
    S->>VAL: Validar rango cilindro (-6 a +6)
    VAL-->>S: Valor válido

    O->>S: Agregar adición presbicia (+1.50)
    S->>VAL: Validar coherencia con edad
    VAL-->>S: Coherente (paciente 45 años)

    O->>S: Guardar prescripción
    S->>VAL: Validar cambios vs anterior
    VAL->>DB: Obtener prescripción previa
    DB-->>VAL: Última prescripción (hace 18 meses)
    VAL->>VAL: Calcular diferencia: +0.75 dioptrías
    
    alt Cambio significativo (>1.0 dioptrías)
        VAL-->>S: Solicitar confirmación
        S->>O: ¿Confirmar cambio mayor?
        O->>S: Confirmar cambio
    else Cambio normal
        VAL-->>S: Cambio normal aprobado
    end

    S->>DB: Guardar nueva prescripción
    DB-->>S: ID prescripción: #5678
    S->>NOT: Programar recordatorio (2 años)
    S->>O: Prescripción creada exitosamente

    Note over O,DB: Prescripción vigente por 24 meses
```

## Secuencia 3: Proceso de Crédito y Pagos

```mermaid
sequenceDiagram
    participant V as Vendedor
    participant S as Sistema
    participant CRED as Módulo Crédito
    participant DB as Base de Datos
    participant EMAIL as Sistema Email
    participant SMS as Sistema SMS

    Note over V,SMS: Otorgamiento y Seguimiento de Crédito

    V->>S: Cliente solicita crédito ($1,200,000)
    S->>CRED: Evaluar capacidad crediticia
    CRED->>DB: Consultar historial pagos
    DB-->>CRED: 3 créditos previos, todos pagados
    CRED->>CRED: Calcular score crediticio: 85/100
    
    alt Score >= 70
        CRED-->>S: Crédito pre-aprobado
        S->>V: Mostrar opciones de cuotas
        
        V->>S: Seleccionar 6 cuotas
        S->>CRED: Calcular plan pagos
        CRED->>CRED: Cuota mensual: $220,000 (interés 2.5%)
        CRED-->>S: Plan generado
        
        S->>V: Mostrar plan al cliente
        V->>S: Cliente acepta términos
        
        S->>DB: Crear registro crédito
        DB-->>S: Crédito #CR-2024-001 creado
        
        S->>EMAIL: Enviar contrato digital
        EMAIL-->>S: Email enviado
        
        S->>SMS: Programar recordatorios
        SMS-->>S: Recordatorios programados
        
    else Score < 70
        CRED-->>S: Crédito rechazado
        S->>V: Mostrar mensaje rechazo
        S->>V: Sugerir alternativas (fiador, menor monto)
    end

    Note over V,SMS: Seguimiento automático activado

    %% Proceso de pago posterior
    rect rgb(240, 248, 255)
        Note over V,SMS: 30 días después - Vencimiento cuota
        
        SMS->>DB: Consultar cuotas por vencer
        DB-->>SMS: Cuota #1 vence mañana
        SMS->>SMS: Enviar recordatorio WhatsApp
        
        V->>S: Cliente realiza pago cuota
        S->>CRED: Registrar pago ($220,000)
        CRED->>DB: Actualizar saldo pendiente
        DB-->>CRED: Saldo: $1,000,000
        CRED->>EMAIL: Enviar confirmación pago
        EMAIL-->>CRED: Comprobante enviado
    end
```

## Secuencia 4: Gestión de Inventario Automática

```mermaid
sequenceDiagram
    participant SISTEMA as Sistema (Cron)
    participant INV as Módulo Inventario
    participant DB as Base de Datos
    participant PROV as Sistema Proveedores
    participant ADMIN as Administrador
    participant EMAIL as Sistema Email

    Note over SISTEMA,EMAIL: Monitoreo Automático de Inventario

    SISTEMA->>INV: Ejecutar verificación diaria (6:00 AM)
    INV->>DB: Consultar productos stock < mínimo
    DB-->>INV: 5 productos críticos encontrados
    
    loop Por cada producto crítico
        INV->>DB: Obtener detalles producto
        DB-->>INV: Montura Ray-Ban: Stock 2, Mínimo 10
        
        INV->>INV: Evaluar rotación producto
        INV->>DB: Consultar ventas últimos 30 días
        DB-->>INV: 15 unidades vendidas/mes
        
        INV->>INV: Calcular cantidad sugerida: 25 unidades
        
        INV->>PROV: Consultar disponibilidad
        PROV-->>INV: Disponible en 5 días, $450,000
        
        INV->>DB: Crear alerta de reposición
    end

    INV->>EMAIL: Enviar reporte administrador
    EMAIL->>ADMIN: "5 productos requieren reposición urgente"
    
    ADMIN->>INV: Revisar alertas pendientes
    INV->>DB: Obtener lista completa
    DB-->>INV: Productos + sugerencias compra
    INV->>ADMIN: Mostrar dashboard inventario

    ADMIN->>INV: Aprobar orden compra automática
    INV->>PROV: Enviar orden compra
    PROV-->>INV: Orden confirmada #OC-2024-045
    
    INV->>DB: Actualizar estado "En pedido"
    INV->>EMAIL: Notificar recepción programada
    
    Note over SISTEMA,EMAIL: Reposición automática completada
```

## Diagramas de Estados

### Estado de una Factura
```mermaid
stateDiagram-v2
    [*] --> Borrador
    Borrador --> Emitida : generar()
    Emitida --> Pagada : registrar_pago()
    Emitida --> Anulada : anular()
    Pagada --> [*]
    Anulada --> [*]
    
    Pagada --> Devolucion : procesar_devolucion()
    Devolucion --> [*]
```

### Estado de un Crédito
```mermaid
stateDiagram-v2
    [*] --> Evaluacion
    Evaluacion --> Aprobado : score >= 70
    Evaluacion --> Rechazado : score < 70
    Aprobado --> Vigente : firmar_contrato()
    Vigente --> Pagado : pagar_todo()
    Vigente --> Mora : vencer_cuota()
    Mora --> Vigente : pagar_mora()
    Mora --> Castigado : mora > 90_dias
    Pagado --> [*]
    Rechazado --> [*]
    Castigado --> [*]
```