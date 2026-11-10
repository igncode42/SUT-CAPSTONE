# Pruebas · Sistema Unidad Territorial

## 1. Objetivo

Verificar que las funcionalidades implementadas del Sistema Unidad Territorial (SUT) cumplan sus reglas de negocio, controles de acceso e integridad esperada.

Las pruebas consideran escenarios válidos, intentos no autorizados, operaciones duplicadas y casos límite.

---

## 2. Estrategia

La verificación combina:

- `TestCase` de Django;
- Django Test Client;
- PostgreSQL;
- backend de correo en memoria para pruebas automatizadas;
- Docker Compose;
- recorridos End to End manuales.

La suite cubre principalmente:

- autenticación y autorización;
- permisos por rol;
- aislamiento de datos;
- validaciones;
- reglas de negocio;
- estados;
- operaciones duplicadas;
- restricciones de base de datos;
- concurrencia;
- fallos controlados de servicios externos.

---

## 3. Niveles de prueba

| Nivel | Estado |
|---|---|
| Automatizadas con Django | **Implementadas** |
| Integración | **Implementada** |
| Funcionales | **Implementadas** |
| End to End manual | **Ejecutado en flujos críticos** |
| End to End automatizado con navegador | **No implementado** |
| Carga / rendimiento | **No ejecutado formalmente** |

No se presentan como ejecutadas pruebas que no cuentan con respaldo verificable.

---

## 4. Suite automatizada

| Aplicación | Pruebas |
|---|---:|
| Usuarios | 20 |
| Vecinos | 13 |
| Proyectos | 19 |
| Certificados | 29 |
| Reservas | 13 |
| Actividades | 16 |
| Comunicaciones | 23 |
| **Total** | **133** |

Último resultado verificado:

```text id="ghy4mk"
Found 133 test(s).
Ran 133 tests
OK
```

La suite completa se ejecutó dentro del entorno Docker.

---

## 5. Cobertura principal

### Usuarios y vecinos

Se verifican:

- registro;
- login y logout;
- creación y edición de perfiles;
- gestión de vecinos;
- membresía;
- permisos por rol;
- aislamiento de información;
- prevención de autoasignación de privilegios.

### Proyectos

Se verifican:

- postulación exclusiva para miembros;
- asociación automática con el vecino;
- estado inicial;
- aislamiento de proyectos;
- aprobación y rechazo;
- prevención de doble resolución;
- estados válidos;
- envío de correo;
- comportamiento ante fallo SMTP.

Un fallo SMTP simulado permite comprobar que una resolución ya registrada no sea revertida.

### Certificados

Se verifican:

- creación de solicitudes;
- aislamiento;
- autorización;
- control de solicitudes activas;
- aprobación y rechazo;
- prevención de doble resolución y emisión;
- snapshot de datos;
- generación de PDF;
- acceso privado al documento;
- envío del PDF por correo;
- comportamiento ante fallos SMTP.

### Reservas

Se verifican:

- creación válida;
- fechas y horarios;
- estados;
- espacios activos;
- detección de solapamientos;
- horarios contiguos;
- reservas propias;
- calendario;
- exclusión de reservas canceladas.

La creación utiliza transacción y bloqueo del espacio antes de confirmar disponibilidad.

### Actividades

Se verifican:

- inscripción;
- prevención de duplicados;
- cupos;
- actividades vigentes;
- restricciones de base de datos;
- creación y edición administrativa;
- gestión de cupos;
- eliminación cuando corresponde;
- protección de actividades con inscritos.

La inscripción utiliza transacción y bloqueo de la actividad.

### Comunicaciones

Se verifican:

- publicación de noticias y avisos;
- permisos;
- acceso público;
- asignación del autor desde servidor;
- creación, edición y eliminación;
- escape de contenido mediante Django Templates.

---

## 6. End to End manual

Se realizaron recorridos manuales sobre los flujos críticos.

### Proyectos

```text id="0q5qgj"
Registro
→ Membresía
→ Postulación
→ Revisión
→ Resolución
→ Correo
```

Se validó el envío real mediante servidor SMTP externo.

### Certificados

```text id="q089z6"
Solicitud
→ Aprobación
→ Emisión
→ PDF
→ Correo
```

Se verificó además la persistencia del estado emitido y el acceso al documento.

### Actividades

```text id="7knu25"
Directiva
→ Crear actividad
→ Editar
→ Gestionar cupos
→ Eliminar cuando corresponde
```

El sistema también fue revisado manualmente en escritorio y dispositivo móvil.

Estos recorridos fueron ejecutados de forma manual y no mediante automatización de navegador.

---

## 7. Ejecución

Suite completa:

```bash id="hwgtcf"
docker compose exec -T web python manage.py test --verbosity 1
```

Verificación de Django:

```bash id="u2g9jy"
docker compose exec -T web python manage.py check
```

Verificación de migraciones pendientes:

```bash id="h8cmvh"
docker compose exec -T web python manage.py makemigrations --check --dry-run
```

Último checkpoint:

```text id="gmlksf"
Django check            OK
Pruebas                 133/133
Migraciones pendientes  ninguna
```

---

## 8. Plan de Pruebas

La suite automatizada y el Plan de Pruebas cumplen funciones distintas:

```text id="u101yf"
Suite automatizada
→ verificación técnica repetible

Plan de Pruebas
→ planificación y registro formal
```

Versiones conservadas:

- `historico/Plan_de_Pruebas_SUT_v0.1.xlsx`: versión histórica;
- `Plan_de_Pruebas_SUT_v0.2.xlsx`: plan formal utilizado para la Entrega 2.2.

La versión v0.2 contiene **28 casos representativos**, todos registrados como ejecutados correctamente.

```text id="bjv4cz"
Casos    28
OK       28
NOK       0
```

La suite automatizada de 133 pruebas constituye el respaldo técnico complementario del sistema.

---

## 9. Límites

No se dispone actualmente de:

- pruebas End to End automatizadas mediante navegador;
- prueba multihilo específica de concurrencia;
- pruebas formales de carga;
- pruebas formales de rendimiento;
- pruebas de disponibilidad productiva.

Estas capacidades no se presentan como ejecutadas ni demostradas.