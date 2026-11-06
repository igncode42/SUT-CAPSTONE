# Matriz de trazabilidad — Sistema Unidad Territorial

## 1. Objetivo

Relacionar los requisitos principales del Sistema Unidad Territorial (SUT) con su implementación, pruebas y respaldo técnico para la Entrega 2.2.

La trazabilidad distingue entre:

`Diseñado ≠ Implementado ≠ Probado ≠ Demostrado`

Un diseño o diagrama describe una solución, pero no acredita por sí solo su funcionamiento.

## 2. Trazabilidad funcional

| Requisito | Resultado implementado | Estado | Respaldo |
|---|---|---|---|
| RF-01 — Gestión de vecinos | Registro, perfil de vecino, gestión interna y control de membresía | **Implementado y probado** | `vecinos/`; `usuarios/permisos.py`; tests de Vecinos y Usuarios |
| RF-02 — Proyectos vecinales | Miembros pueden postular; Directiva/personal autorizado puede aprobar o rechazar | **Implementado y probado** | `proyectos/`; tests de Proyectos |
| RF-03 — Resolución por correo | La resolución se notifica al postulante y una falla SMTP no revierte la decisión | **Implementado, probado y demostrado** | `proyectos/notificaciones.py`; tests; recorrido SMTP controlado |
| RF-04 — Certificados de residencia | Solicitud, revisión, aprobación/rechazo y emisión | **Implementado y probado** | `certificados/`; tests de Certificados |
| RF-05 — Reservas de espacios | Reserva, calendario, validación temporal y detección de solapamientos | **Implementado y probado** | `reservas/`; tests de Reservas |
| RF-06 — Actividades y cupos | Consulta, inscripción, prevención de duplicados y control de capacidad | **Implementado y probado** | `actividades/`; tests de Actividades |
| RF-07 — Noticias y avisos | Publicación autorizada y consulta de comunicaciones | **Implementado y probado** | `comunicaciones/`; tests de Comunicaciones |
| RF-08 — Autenticación y autorización | Login, roles, permisos y aislamiento de información | **Implementado y probado** | `usuarios/`; `usuarios/permisos.py`; tests de Usuarios |
| APT — Interfaz web responsiva | Interfaz basada en Django Templates y Bootstrap | **Implementado y revisado** | `templates/`; revisión funcional responsive |
| APT — Persistencia de datos | Datos almacenados mediante Django ORM y PostgreSQL | **Implementado y probado** | modelos, migraciones y PostgreSQL |

## 3. Reglas e integridad

| Regla | Resultado implementado | Estado | Respaldo |
|---|---|---|---|
| Sólo miembros pueden postular proyectos | Permiso validado en servidor | **Probado** | `usuarios/permisos.py`; tests de Proyectos |
| Sólo perfiles autorizados resuelven proyectos y certificados | Autorización centralizada | **Probado** | `usuarios/permisos.py`; tests negativos |
| Un proyecto no puede resolverse dos veces | Estado validado y operación protegida mediante transacción | **Probado** | `proyectos/views.py`; tests |
| Un vecino no puede mantener múltiples solicitudes activas de certificado | Restricción de base de datos y validación de flujo | **Probado** | modelos/migraciones de Certificados |
| Un certificado no puede emitirse dos veces | Estado y flujo de emisión controlados | **Probado** | `certificados/views.py`; tests |
| Los certificados conservan los datos utilizados en su emisión | Snapshot de identidad y dirección | **Probado** | `certificados/models.py`; tests |
| Una reserva debe tener inicio anterior al término | Validación y `CheckConstraint` PostgreSQL | **Probado** | `reservas/models.py`; tests |
| No deben existir reservas superpuestas durante el flujo normal | Validación de solapamientos y revalidación bajo bloqueo del espacio | **Probado funcionalmente** | `reservas/forms.py`; `reservas/views.py`; tests |
| Las inscripciones dependen del cupo disponible | Control bajo transacción y bloqueo de actividad | **Probado funcionalmente** | `actividades/views.py`; tests |
| No se permiten inscripciones duplicadas | Restricción única vecino/actividad | **Probado** | `actividades/models.py`; tests |

## 4. Seguridad y acceso

| Requisito | Resultado | Estado / respaldo |
|---|---|---|
| Autenticación | Login y logout mediante Django | **Implementado y probado** |
| Autorización | Permisos centralizados por rol y perfil | **Implementado y probado** |
| Aislamiento de datos | Usuarios acceden únicamente a la información que les corresponde | **Implementado y probado** |
| Protección CSRF | Middleware y formularios Django | **Implementado** |
| Secretos fuera del repositorio | Configuración mediante variables de entorno | **Verificado** |
| Integridad de estados | Constraints PostgreSQL en operaciones críticas | **Implementado y probado** |
| Contenedor sin privilegios root | Proceso web ejecutado por usuario `sut` | **Verificado** |
| Contenido de comunicaciones | Escape automático de Django Templates | **Probado** |

Auditorías complementarias realizadas durante el hardening:

```text
Gitleaks       → sin filtraciones detectadas
pip-audit      → sin vulnerabilidades conocidas detectadas
check --deploy → sin observaciones bajo perfil de producción simulado
```

## 5. Trazabilidad técnica de Capstone

| Elemento solicitado | Estado actual | Respaldo |
|---|---|---|
| Arquitectura | **Implementada y documentada** | `docs/diagramas/01-arquitectura-sut.svg`; `config/`; Docker |
| Modelo de datos | **Implementado** | modelos Django, 15 migraciones y PostgreSQL |
| Procesos principales | **Documentados** | diagramas de Proyectos, Reservas y Actividades |
| Dockerización | **Implementada y verificada** | `Dockerfile`; `compose.yml`; `.dockerignore` |
| Requisitos funcionales y no funcionales | **Documentados** | `docs/especificaciones/especificaciones-tecnicas.md` |
| Pruebas automatizadas | **97/97 aprobadas** | archivos de tests; `docs/pruebas/` |
| Plan formal de pruebas | v0.1 histórico; v0.2 pendiente de cierre | `docs/pruebas/` |
| Control de versiones | **Implementado** | Git / GitHub |
| Gestión del trabajo | Scrum mediante Jira | tablero Jira; sincronización final 2.2 pendiente |
| Evidencias | Histórico disponible; evidencia final 2.2 pendiente de consolidación | `docs/evidencias/` |
| Documentación de cierre | 2.1 histórica; cierre 2.2 pendiente | `docs/cierre/` |

## 6. Estado de pruebas

Suite automática actual:

```text
Usuarios          16
Vecinos           13
Proyectos         19
Certificados      20
Reservas          13
Actividades        7
Comunicaciones     9
────────────────────
Total             97
```

Último resultado verificado:

```text
97 pruebas ejecutadas
97 aprobadas
0 fallidas
```

También se ejecutaron recorridos End to End manuales de:

- postulación, resolución y notificación de Proyecto;
- solicitud, aprobación y emisión de Certificado.

No se dispone actualmente de pruebas End to End automatizadas mediante navegador.

## 7. Límites actuales

No se presentan como implementadas:

- integración con WhatsApp;
- certificado descargable en PDF;
- pruebas End to End automatizadas con navegador;
- despliegue productivo externo;
- pruebas formales de carga o rendimiento.

Estas capacidades no son necesarias para acreditar las funcionalidades actualmente implementadas y quedan fuera de la demostración técnica actual.

## 8. Regla de trazabilidad

La cadena utilizada durante el proyecto es:

`Requisito → Jira → Implementación → Prueba → Commit → Evidencia → Documentación`

Para la Entrega 2.2, Jira, evidencias y documentación se sincronizan con el estado técnico final antes de preparar la presentación y demostración.