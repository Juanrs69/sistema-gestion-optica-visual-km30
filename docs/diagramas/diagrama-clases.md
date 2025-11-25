# Diagrama de Clases - Sistema Óptica Visual Km 30

```mermaid
classDiagram
    %% Clase Usuario y Autenticación
    class User {
        +int id
        +string username
        +string email
        +string password_hash
        +datetime created_at
        +boolean is_active
        +string rol
        +login()
        +logout()
        +change_password()
    }

    %% Clase Paciente
    class Paciente {
        +int id
        +string tipo_documento
        +string numero_documento
        +string nombres
        +string apellidos
        +date fecha_nacimiento
        +string telefono
        +string email
        +string direccion
        +text observaciones
        +datetime fecha_registro
        +datetime fecha_actualizacion
        +boolean activo
        +get_nombre_completo()
        +get_edad()
        +get_historial_prescripciones()
        +get_facturas()
    }

    %% Clase Prescripción
    class Prescripcion {
        +int id
        +int paciente_id
        +date fecha_examen
        +string profesional
        +decimal od_esfera
        +decimal od_cilindro
        +int od_eje
        +decimal os_esfera
        +decimal os_cilindro
        +int os_eje
        +decimal adicion
        +decimal distancia_pupilar
        +text observaciones
        +datetime fecha_registro
        +boolean vigente
        +validar_vigencia()
        +calcular_diferencia_anterior()
    }

    %% Clase Producto
    class Producto {
        +int id
        +string codigo
        +string nombre
        +string categoria
        +string marca
        +string modelo
        +text descripcion
        +decimal precio_compra
        +decimal precio_venta
        +int stock_actual
        +int stock_minimo
        +string imagen_url
        +boolean activo
        +datetime fecha_registro
        +verificar_disponibilidad()
        +actualizar_stock()
        +calcular_margen()
    }

    %% Clase Categoría de Producto
    class CategoriaProducto {
        +int id
        +string nombre
        +string descripcion
        +string codigo
        +boolean activo
    }

    %% Clase Factura
    class Factura {
        +int id
        +string numero_factura
        +int paciente_id
        +date fecha
        +decimal subtotal
        +decimal descuentos
        +decimal impuestos
        +decimal total
        +string estado
        +string forma_pago
        +text observaciones
        +datetime fecha_registro
        +calcular_totales()
        +generar_factura_electronica()
        +anular()
    }

    %% Clase Detalle de Factura
    class DetalleFactura {
        +int id
        +int factura_id
        +int producto_id
        +int prescripcion_id
        +int cantidad
        +decimal precio_unitario
        +decimal subtotal
        +text especificaciones
        +calcular_subtotal()
    }

    %% Clase Crédito
    class Credito {
        +int id
        +int factura_id
        +decimal valor_total
        +decimal valor_pagado
        +decimal saldo_pendiente
        +int numero_cuotas
        +decimal valor_cuota
        +decimal interes_mensual
        +date fecha_vencimiento
        +string estado
        +datetime fecha_creacion
        +generar_plan_pagos()
        +registrar_pago()
        +calcular_mora()
    }

    %% Clase Pago de Crédito
    class PagoCredito {
        +int id
        +int credito_id
        +decimal valor_pago
        +date fecha_pago
        +string medio_pago
        +string comprobante
        +text observaciones
        +datetime fecha_registro
    }

    %% Clase Inventario (Movimientos)
    class MovimientoInventario {
        +int id
        +int producto_id
        +string tipo_movimiento
        +int cantidad
        +string concepto
        +string referencia_documento
        +datetime fecha_movimiento
        +int usuario_id
    }

    %% Clase Proveedor
    class Proveedor {
        +int id
        +string nit
        +string razon_social
        +string contacto
        +string telefono
        +string email
        +string direccion
        +boolean activo
    }

    %% Clase Orden de Trabajo
    class OrdenTrabajo {
        +int id
        +int prescripcion_id
        +int paciente_id
        +string numero_orden
        +date fecha_orden
        +date fecha_entrega_estimada
        +date fecha_entrega_real
        +string estado
        +text especificaciones
        +decimal precio_estimado
        +text observaciones
        +actualizar_estado()
        +calcular_tiempo_fabricacion()
    }

    %% Clase Campaña Marketing
    class CampanaMarketing {
        +int id
        +string nombre
        +text descripcion
        +date fecha_inicio
        +date fecha_fin
        +string tipo_campana
        +string canal
        +text mensaje
        +boolean activa
        +enviar_campana()
        +obtener_estadisticas()
    }

    %% Relaciones
    Paciente ||--o{ Prescripcion : "tiene"
    Paciente ||--o{ Factura : "compra"
    Factura ||--o{ DetalleFactura : "contiene"
    Producto ||--o{ DetalleFactura : "se vende en"
    Prescripcion ||--o{ DetalleFactura : "especifica"
    CategoriaProducto ||--o{ Producto : "clasifica"
    Factura ||--o| Credito : "genera"
    Credito ||--o{ PagoCredito : "recibe"
    Producto ||--o{ MovimientoInventario : "registra"
    User ||--o{ MovimientoInventario : "ejecuta"
    Proveedor ||--o{ Producto : "suministra"
    Prescripcion ||--o{ OrdenTrabajo : "genera"
    User ||--o{ Prescripcion : "crea"
    User ||--o{ Factura : "emite"

    %% Estilos
    classDef entityClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef valueClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef serviceClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px

    class Paciente,Producto,Factura entityClass
    class DetalleFactura,PagoCredito,MovimientoInventario valueClass
    class User,CampanaMarketing,OrdenTrabajo serviceClass
```

## Descripción de las Clases Principales

### 🏢 **Entidades de Negocio**

#### **Paciente**
- **Propósito**: Gestionar información personal y médica de clientes
- **Responsabilidades**: Validar datos, calcular edad, mantener historial
- **Relaciones**: Uno a muchos con Prescripciones y Facturas

#### **Prescripcion** 
- **Propósito**: Almacenar fórmulas oftalmológicas
- **Responsabilidades**: Validar rangos de dioptrías, verificar vigencia
- **Reglas de Negocio**: Vigencia 2 años, solo optómetras pueden crear

#### **Producto**
- **Propósito**: Catálogo de inventario (monturas, lentes, accesorios)
- **Responsabilidades**: Control de stock, cálculo de márgenes
- **Categorías**: Monturas, Lentes oftálmicos, Lentes contacto, Accesorios

#### **Factura**
- **Propósito**: Documento de venta oficial
- **Responsabilidades**: Cálculos tributarios, facturación electrónica
- **Estados**: Borrador, Emitida, Pagada, Anulada

### 💰 **Entidades Financieras**

#### **Credito**
- **Propósito**: Gestionar ventas a crédito
- **Responsabilidades**: Plan de pagos, cálculo de intereses, control de mora
- **Límites**: Máximo 12 cuotas, evaluación crediticia

#### **PagoCredito**
- **Propósito**: Registrar abonos a créditos
- **Medios**: Efectivo, Transferencia, Tarjeta

### 📦 **Control de Inventario**

#### **MovimientoInventario**
- **Tipos**: Entrada, Salida, Ajuste, Devolución
- **Trazabilidad**: Usuario responsable, fecha, documento referencia

### 🔧 **Servicios y Procesos**

#### **OrdenTrabajo**
- **Propósito**: Coordinar fabricación de lentes graduados
- **Estados**: Pendiente, En Proceso, Terminada, Entregada
- **Integración**: Con prescripción y productos