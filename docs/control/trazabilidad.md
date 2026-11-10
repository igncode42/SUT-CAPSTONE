# Matriz de trazabilidad · Sistema Unidad Territorial

## 1. Objetivo

Relacionar los principales requisitos del Sistema Unidad Territorial (SUT) con su implementación, verificación y respaldo técnico.

La trazabilidad mantiene la distinción:

```text
Diseñado ≠ Implementado ≠ Probado ≠ Demostrado
```

Un diseño o documento describe una solución, pero no acredita por sí solo su funcionamiento.

---

## 2. Trazabilidad funcional

| Requisito | Resultado | Estado | Respaldo |
|---|---|---|---|
| RF-01 · Gestión de vecinos | Registro, perfil, gestión interna y membresía | **Implementado y probado** | `vecinos/`; `usuarios/permisos.py`; tests |
| RF-02 · Proyectos vecinales | Postulación por miembros y resolución por usuarios autorizados | **Implementado y probado** | `proyectos/`; tests |
| RF-03 · Resolución por correo | Aprobación/rechazo notificado por email sin revertir la resolución ante fallo SMTP | **Implementado, probado y demostrado** | `proyectos/notificaciones.py`; tests; recorrido SMTP |
| RF-04 · Certificados | Solicitud, revisión, resolución, emisión y PDF | **Implementado, probado y demostrado** | `certificados/`; tests; recorrido funcional |
| RF-05 · Reservas | Reserva, calendario, validación temporal y control de solapamientos | **Implementado y probado** | `reservas/`; tests |
| RF-06 · Actividades | Consulta, inscripción, cupos y gestión administrativa | **Implementado y probado** | `actividades/`; tests |
| RF-07 · Comunicaciones | Noticias, avisos y gestión por usuarios autorizados | **Implementado y probado** | `comunicaciones/`; tests |
| RF-08 · Autenticación y autorización | Login, roles, permisos y aislamiento de información | **Implementado y probado** | `usuarios/`; `usuarios/permisos.py`; tests |
| APT · Interfaz responsiva | Interfaz web adaptable | **Implementado y verificado** | `templates/`; Bootstrap; pruebas manuales en escritorio y móvil |
| APT · Persistencia | Persistencia relacional mediante PostgreSQL | **Implementado y probado** | modelos; migraciones; PostgreSQL |

---

## 3. Reglas e integridad

| Regla | Implementación | Estado | Respaldo |
|---|---|---|---|
| Sólo miembros pueden postular proyectos | Validación desde servidor | **Probado** | permisos y tests de Proyectos |
| Sólo usuarios autorizados pueden resolver | Autorización centralizada | **Probado** | `usuarios/permisos.py`; tests negativos |
| Un proyecto no puede resolverse dos veces | Estado + transacción + bloqueo | **Probado** | `proyectos/views.py`; tests |
| No pueden coexistir solicitudes activas de certificado para un mismo vecino | Validación y restricción de datos | **Probado** | modelos, migraciones y tests |
| Un certificado no puede emitirse dos veces | Estado + transacción + bloqueo | **Probado** | `certificados/`; tests |
| El certificado conserva los datos usados en su emisión | Snapshot de datos del vecino | **Probado** | modelo y tests |
| El PDF sólo puede accederse desde la cuenta correspondiente | Control de acceso en servidor | **Probado** | vistas y tests de Certificados |
| Una reserva debe tener inicio anterior al término | Validación + constraint | **Probado** | modelos y tests de Reservas |
| Las reservas no deben solaparse | Validación y revalidación bajo bloqueo | **Probado** | formularios, vistas y tests |
| Las inscripciones dependen del cupo disponible | Transacción y bloqueo de actividad | **Probado** | vistas y tests de Actividades |
| No se permiten inscripciones duplicadas | Restricción vecino/actividad | **Probado** | modelo y tests |

---

## 4. Seguridad y requisitos técnicos

| Requisito | Resultado | Estado |
|---|---|---|
| Autenticación | Login y logout mediante Django | **Implementado y probado** |
| Autorización | Permisos centralizados por rol y perfil | **Implementado y probado** |
| Aislamiento de información | Acceso limitado a información correspondiente al usuario | **Implementado y probado** |
| Protección CSRF | Middleware y formularios Django | **Implementado** |
| Secretos fuera del repositorio | Variables de entorno y `.env` excluido | **Verificado** |
| Integridad de datos | Validaciones y constraints PostgreSQL | **Implementado y probado** |
| Concurrencia | `transaction.atomic()` y `select_for_update()` | **Implementado y probado** |
| Contenedor sin privilegios root | Proceso web ejecutado con usuario no privilegiado | **Verificado** |
| Escape de contenido | Escape automático mediante Django Templates | **Implementado y probado** |
| Entorno reproducible | Dockerfile + Docker Compose | **Implementado y verificado** |

---

## 5. Trazabilidad técnica de Capstone

| Elemento | Estado | Respaldo |
|---|---|---|
| Arquitectura | **Implementada y documentada** | `docs/diagramas/01-arquitectura-sut.svg`; Docker; `config/` |
| Modelo de datos | **Implementado y documentado** | modelos Django; 15 migraciones; PostgreSQL |
| Procesos principales | **Documentados** | `docs/diagramas/` |
| Dockerización | **Implementada y verificada** | `Dockerfile`; `compose.yml`; `.dockerignore` |
| Requisitos técnicos | **Documentados** | `docs/especificaciones/especificaciones-tecnicas.md` |
| Pruebas automatizadas | **133/133 aprobadas** | archivos de tests |
| Plan formal de pruebas | **v0.2 completado** | `docs/pruebas/Plan_de_Pruebas_SUT_v0.2.xlsx` |
| End to End | **Recorridos críticos ejecutados** | pruebas manuales de Proyectos, Certificados y Actividades |
| Responsive | **Verificado** | escritorio y dispositivo móvil |
| SMTP | **Verificado** | recorridos funcionales de correo |
| PDF de certificados | **Implementado y verificado** | módulo Certificados; pruebas; recorrido funcional |
| Control de versiones | **Implementado** | Git / GitHub |
| Gestión del trabajo | **En uso** | Jira |
| Evidencias | **Histórico organizado; consolidación final pendiente** | `docs/evidencias/` |
| Documentación de cierre | **En actualización para v1.0** | `docs/cierre/` |

---

## 6. Estado de pruebas

Suite automatizada:

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

Último resultado:

```text
133 pruebas ejecutadas
133 aprobadas
0 fallidas
```

Plan formal de pruebas v0.2:

```text
Casos representativos    28
OK                       28
NOK                       0
No ejecutados             0
Avance                  100 %
```

Además, se realizaron recorridos manuales sobre los flujos críticos y validaciones en escritorio y dispositivo móvil.

No se dispone de pruebas End to End automatizadas mediante navegador.

---

## 7. Límites de la versión v1.0

No se presentan como implementadas:

- integración directa con WhatsApp;
- pruebas End to End automatizadas mediante navegador;
- despliegue productivo en infraestructura externa;
- pruebas formales de carga o rendimiento.

Estas capacidades quedan fuera del alcance demostrado de la versión v1.0.

---

## 8. Regla de trazabilidad

La cadena utilizada durante el proyecto es:

```text
Requisito
    ↓
Jira
    ↓
Implementación
    ↓
Prueba
    ↓
Commit
    ↓
Evidencia
    ↓
Documentación
```

La documentación técnica y el producto se encuentran alineados con el estado funcional de **SUT v1.0**.

La consolidación final de Jira y evidencias se realiza como parte del cierre documental del proyecto.