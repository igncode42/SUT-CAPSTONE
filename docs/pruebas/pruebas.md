# Pruebas · Sistema Unidad Territorial

## 1. Objetivo

Verificar que las funcionalidades implementadas del Sistema Unidad Territorial (SUT) cumplan sus reglas de negocio, controles de acceso e integridad.

Las pruebas consideran escenarios válidos, accesos no autorizados, operaciones duplicadas, casos límite y fallos controlados.

---

## 2. Estrategia

La verificación combina:

- Django `TestCase` y Test Client;
- PostgreSQL;
- backend de correo en memoria para pruebas automatizadas;
- Docker Compose;
- recorridos manuales End to End.

La suite cubre principalmente:

- autenticación y autorización;
- permisos por rol;
- aislamiento de información;
- validaciones y reglas de negocio;
- estados y operaciones duplicadas;
- restricciones de base de datos;
- operaciones protegidas mediante transacciones y bloqueos;
- fallos controlados de servicios externos.

---

## 3. Niveles de prueba

| Nivel | Estado |
|---|---|
| Unitarias / de componente | **Incluidas en la suite automatizada** |
| Funcionales | **Implementadas** |
| Integración | **Implementada** |
| Aceptación | **Verificada mediante criterios del plan y recorridos manuales** |
| End to End manual | **Ejecutado en flujos críticos** |
| End to End automatizado con navegador | **No implementado** |
| Carga / rendimiento | **No ejecutado formalmente** |

No se realizó una prueba formal de aceptación con cliente. Los criterios de aceptación se verificaron mediante el Plan de Pruebas y recorridos manuales del sistema.

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

```text id="2hqpxh"
Found 133 test(s).
Ran 133 tests
OK
```

La suite completa se ejecutó dentro del entorno Docker.

Respaldo: `docs/evidencias/fase-2.2/27-pruebas-133-ok.png`.

---

## 5. Cobertura principal

### Usuarios y vecinos

Se verifican registro, autenticación, perfiles, gestión de vecinos, membresía, permisos por rol, aislamiento de información y prevención de autoasignación de privilegios.

### Proyectos

Se verifican postulación por miembros, estados, aislamiento, aprobación y rechazo, prevención de doble resolución, notificación por correo y comportamiento ante fallo SMTP.

Un fallo SMTP simulado comprueba que una resolución ya registrada no sea revertida.

### Certificados

Se verifican solicitudes, autorización, aislamiento, solicitudes activas, resolución, prevención de doble emisión, snapshot de datos, generación y acceso privado al PDF, correo y fallos SMTP.

### Reservas

Se verifican fechas y horarios, espacios activos, estados, solapamientos, horarios contiguos, reservas propias y calendario.

La creación utiliza transacción y bloqueo del espacio antes de confirmar disponibilidad.

### Actividades

Se verifican inscripción, duplicados, cupos, vigencia, gestión administrativa y protección de actividades con inscritos.

La inscripción utiliza transacción y bloqueo de la actividad.

### Comunicaciones

Se verifican publicación de noticias y avisos, permisos, acceso público, asignación de autor y operaciones de creación, edición y eliminación.

---

## 6. Recorridos End to End manuales

Se ejecutaron recorridos completos sobre los principales flujos del sistema.

### Proyectos

```text id="dww3x1"
Postulación
→ Revisión
→ Resolución
→ Actualización de estado
→ Correo
```

Respaldo: evidencia 29.

### Certificados

```text id="nzmd2u"
Solicitud
→ Aprobación
→ Emisión
→ PDF
→ Correo
```

Se verificó además el estado emitido y el acceso al documento.

Respaldo: evidencia 30.

### Reservas

```text id="beyifh"
Crear reserva
→ Confirmación
→ Mis reservas
→ Calendario
```

Respaldo: evidencia 31.

### Actividades

```text id="60n98x"
Crear actividad
→ Inscripción
→ Actualización de cupos
→ Consulta
```

Respaldo: evidencia 32.

### Comunicaciones

```text id="oq9vtg"
Publicación
→ Acceso público
→ Visualización responsive
```

Respaldo: evidencia 33.

Los recorridos fueron ejecutados manualmente y no mediante automatización de navegador.

---

## 7. Ejecución y checkpoint

Suite completa:

```bash id="igduvw"
docker compose exec -T web python manage.py test --verbosity 1
```

Verificación de Django:

```bash id="gn0wuf"
docker compose exec -T web python manage.py check
```

Migraciones pendientes:

```bash id="82jnso"
docker compose exec -T web python manage.py makemigrations --check --dry-run
```

Último checkpoint:

```text id="p7drrv"
Django check            OK
Pruebas                 133/133
Migraciones pendientes  ninguna
```

---

## 8. Plan de Pruebas

La suite automatizada y el Plan de Pruebas tienen funciones complementarias:

```text id="2pzb6o"
Suite automatizada
→ verificación técnica repetible

Plan de Pruebas
→ planificación y registro formal
```

Versiones conservadas:

- `historico/Plan_de_Pruebas_SUT_v0.1.xlsx`: versión histórica;
- `Plan_de_Pruebas_SUT_v0.2.xlsx`: versión utilizada para la Entrega 2.2.

Resultado del Plan v0.2:

```text id="4poc00"
Casos representativos    28
OK                       28
NOK                       0
No ejecutados             0
Avance                  100 %
```

La suite de 133 pruebas constituye el respaldo técnico complementario.

---

## 9. Límites

No forman parte del alcance demostrado:

- pruebas End to End automatizadas mediante navegador;
- prueba multihilo específica de concurrencia;
- pruebas formales de carga o rendimiento;
- pruebas de disponibilidad productiva.
