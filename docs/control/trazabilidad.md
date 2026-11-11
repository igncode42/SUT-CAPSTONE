# Matriz de trazabilidad · Sistema Unidad Territorial

## 1. Objetivo

Relacionar los principales requisitos del Sistema Unidad Territorial (SUT) con su implementación, verificación y respaldo.

Se mantiene la distinción:

```text
Diseñado ≠ Implementado ≠ Probado ≠ Demostrado
```

Un diseño o documento describe una solución, pero no acredita por sí solo su funcionamiento.

---

## 2. Trazabilidad funcional

| Requisito | Resultado | Estado | Respaldo |
|---|---|---|---|
| RF-01 · Gestión de vecinos | Registro, perfil, gestión interna y membresía | **Implementado y probado** | `vecinos/`; `usuarios/permisos.py`; tests |
| RF-02 · Proyectos vecinales | Postulación por miembros y resolución por usuarios autorizados | **Implementado, probado y demostrado** | `proyectos/`; tests; evidencia 29 |
| RF-03 · Resolución por correo | Notificación de aprobación o rechazo sin revertir la resolución ante fallo SMTP | **Implementado, probado y demostrado** | `proyectos/notificaciones.py`; tests; evidencia 29 |
| RF-04 · Certificados | Solicitud, resolución, emisión, consulta y PDF | **Implementado, probado y demostrado** | `certificados/`; tests; evidencia 30 |
| RF-05 · Reservas | Reserva, calendario, validación temporal y control de solapamientos | **Implementado, probado y demostrado** | `reservas/`; tests; evidencia 31 |
| RF-06 · Actividades | Consulta, inscripción, cupos y gestión administrativa | **Implementado, probado y demostrado** | `actividades/`; tests; evidencia 32 |
| RF-07 · Comunicaciones | Noticias, avisos y gestión por usuarios autorizados | **Implementado, probado y demostrado** | `comunicaciones/`; tests; evidencia 33 |
| RF-08 · Autenticación y autorización | Login, roles, permisos y aislamiento de información | **Implementado y probado** | `usuarios/`; `usuarios/permisos.py`; tests |
| APT · Interfaz responsiva | Interfaz adaptable a escritorio y móvil | **Implementado y verificado** | `templates/`; Bootstrap; evidencia 33 |
| APT · Persistencia | Persistencia relacional mediante PostgreSQL | **Implementado y probado** | modelos; migraciones; PostgreSQL |

---

## 3. Reglas e integridad

| Regla | Implementación | Estado | Respaldo |
|---|---|---|---|
| Sólo miembros pueden postular proyectos | Validación desde servidor | **Probado** | permisos y tests de Proyectos |
| Sólo usuarios autorizados pueden resolver | Autorización centralizada | **Probado** | `usuarios/permisos.py`; tests negativos |
| Un proyecto no puede resolverse dos veces | Estado, transacción y bloqueo | **Probado** | `proyectos/views.py`; tests |
| No pueden coexistir solicitudes activas de certificado para un mismo vecino | Validación y restricción de datos | **Probado** | modelos, migraciones y tests |
| Un certificado no puede emitirse dos veces | Estado, transacción y bloqueo | **Probado** | `certificados/`; tests |
| El certificado conserva los datos utilizados en su emisión | Snapshot de datos del vecino | **Probado** | modelo y tests |
| El PDF sólo puede accederse desde la cuenta correspondiente | Control de acceso en servidor | **Probado** | vistas y tests de Certificados |
| Una reserva debe tener inicio anterior al término | Validación y constraint | **Probado** | modelos y tests de Reservas |
| Las reservas no deben solaparse | Validación y revalidación bajo bloqueo | **Probado** | formularios, vistas y tests |
| Las inscripciones dependen del cupo disponible | Transacción y bloqueo de actividad | **Probado** | vistas y tests de Actividades |
| No se permiten inscripciones duplicadas | Restricción vecino/actividad | **Probado** | modelo y tests |

---

## 4. Seguridad y requisitos técnicos

| Requisito | Resultado | Estado |
|---|---|---|
| Autenticación | Login y logout mediante Django | **Implementado y probado** |
| Autorización | Permisos centralizados por rol y perfil | **Implementado y probado** |
| Aislamiento de información | Acceso limitado según usuario y permisos | **Implementado y probado** |
| Protección CSRF | Middleware y formularios Django | **Implementado** |
| Secretos fuera del repositorio | Variables de entorno y `.env` excluido | **Verificado** |
| Integridad de datos | Validaciones y constraints PostgreSQL | **Implementado y probado** |
| Control de concurrencia | `transaction.atomic()` y `select_for_update()` en operaciones sensibles | **Implementado; sin prueba multihilo específica** |
| Contenedor sin privilegios root | Proceso web ejecutado con usuario `sut` | **Verificado** |
| Escape de contenido | Escape automático mediante Django Templates | **Implementado** |
| Entorno reproducible | Dockerfile + Docker Compose | **Implementado y verificado** |
| Secret scanning | Revisión del historial mediante Gitleaks | **Verificado** |
| Dependencias Python | Auditoría mediante pip-audit | **Verificado** |
| Configuración Django | `check --deploy` con perfil seguro simulado | **Verificado** |

Respaldo principal: `docs/evidencias/fase-2.2/28-seguridad-checks-ok.png`.

---

## 5. Trazabilidad técnica de Capstone

| Elemento | Estado | Respaldo |
|---|---|---|
| Arquitectura | **Implementada y documentada** | `docs/diagramas/01-arquitectura-sut.svg`; Docker; `config/` |
| Modelo de datos | **Implementado y documentado** | modelos Django; 15 migraciones; PostgreSQL |
| Procesos principales | **Documentados** | `docs/diagramas/` |
| UML y BPMN | **Documentados** | diagramas 06 y 07 |
| Dockerización | **Implementada y verificada** | `Dockerfile`; `compose.yml`; `.dockerignore`; evidencia 26 |
| Requisitos técnicos | **Documentados** | `docs/especificaciones/especificaciones-tecnicas.md` |
| Pruebas automatizadas | **133/133 aprobadas** | tests; evidencia 27 |
| Plan formal de pruebas | **v0.2 completado** | `docs/pruebas/Plan_de_Pruebas_SUT_v0.2.xlsx` |
| End to End manual | **Recorridos críticos ejecutados** | evidencias 29–33 |
| Responsive | **Verificado** | evidencia 33 |
| SMTP | **Verificado** | evidencias 29 y 30 |
| PDF de certificados | **Implementado y verificado** | Certificados; tests; evidencia 30 |
| Seguridad y calidad | **Verificada** | evidencia 28 |
| Control de versiones | **En uso** | Git / GitHub |
| Gestión del trabajo | **En uso y respaldada** | Jira; evidencia 34 |
| Evidencias | **Consolidadas para la Entrega 2.2** | `docs/evidencias/fase-2.2/` |
| Documentación de cierre | **Actualizada para v1.0** | `docs/cierre/` |

---

## 6. Estado de pruebas

### Suite automatizada

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

Resultado:

```text
133 pruebas ejecutadas
133 aprobadas
0 fallidas
```

### Plan formal v0.2

```text
Casos representativos     28
OK                        28
NOK                        0
No ejecutados              0
Avance                   100 %
```

También se ejecutaron recorridos manuales sobre los principales flujos funcionales y validaciones en escritorio y móvil.

Los mecanismos de control de concurrencia utilizan transacciones y bloqueos en operaciones sensibles. No se realizó una prueba multihilo específica.

No se implementaron pruebas End to End automatizadas mediante navegador.

---

## 7. Límites de la versión v1.0

No forman parte del alcance demostrado:

- integración directa con WhatsApp;
- pruebas End to End automatizadas mediante navegador;
- despliegue productivo en infraestructura externa;
- pruebas formales de carga o rendimiento.

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

El producto, las pruebas, Jira y la documentación técnica se encuentran alineados con el estado funcional demostrado de **SUT v1.0**.

Las evidencias correspondientes a la Entrega 2.2 se encuentran consolidadas en `docs/evidencias/fase-2.2/`.