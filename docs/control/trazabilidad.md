# Matriz de trazabilidad — Sistema Unidad Territorial

## 1. Objetivo

Relacionar las necesidades y reglas del Sistema Unidad Territorial (SUT) con su implementación real, estado actual y evidencia técnica.

Esta matriz distingue entre:

- **Implementado y probado:** existe un flujo funcional y cuenta con pruebas automatizadas.
- **Implementado parcialmente:** existe parte de la solución, pero el flujo completo todavía no está disponible.
- **Diseñado / pendiente:** existe definición o diseño, pero aún no existe implementación funcional suficiente.

Un diagrama o modelo representa diseño; por sí solo no demuestra que una funcionalidad esté implementada.

---

## 2. Trazabilidad funcional

| Necesidad / regla | Requisito | Implementación actual | Estado | Evidencia técnica |
|---|---|---|---|---|
| Gestionar vecinos | RF-01 | Modelo `Vecino`, relación con `Usuario`, migración, tabla PostgreSQL y administración Django | **Implementado parcialmente:** base de datos y perfil disponibles; registro/autogestión para usuario final pendiente | `vecinos/models.py`; `vecinos/admin.py`; `docs/diagramas/02-modelo-datos-sut.*` |
| Solicitar y emitir certificados | RF-03 / RF-04 | `SolicitudCertificado` y `Certificado`; solicitud por vecino autenticado; seguimiento; revisión; aprobación/rechazo; emisión lógica | **Implementado y probado:** flujo principal funcional. Generación de PDF/archivo descargable pendiente | `certificados/models.py`; `certificados/views.py`; `certificados/tests.py`; `certificados/test_gestion.py`; `templates/certificados/` |
| Sólo miembros postulan proyectos | RN-01 / RF-05 | Permiso de miembro de junta aplicado en servidor; creación asociada automáticamente al vecino autenticado | **Implementado y probado** | `usuarios/permisos.py`; `proyectos/forms.py`; `proyectos/views.py`; `proyectos/tests.py` |
| Directiva aprueba o rechaza proyectos | RN-02 / RF-06 | Acceso restringido a personal autorizado; listado de pendientes; aprobación/rechazo; protección contra doble resolución | **Implementado y probado** | `usuarios/permisos.py`; `proyectos/views.py`; `proyectos/test_revision.py`; `templates/proyectos/pendientes.html` |
| Notificar resolución de proyectos | Propuesta APT | Servicio de correo Django ejecutado al aprobar o rechazar proyectos | **Implementado y probado en entorno de desarrollo:** integración SMTP externa pendiente | `proyectos/notificaciones.py`; `proyectos/test_notificaciones.py`; `config/settings.py` |
| Reservar espacios comunitarios | RN-04 / RF-09 | Modelos `Espacio` y `Reserva`, migraciones, persistencia y administración | **Implementado parcialmente:** calendario, flujo para usuario final y validación funcional de disponibilidad pendientes | `reservas/models.py`; `reservas/admin.py`; `docs/diagramas/04-proceso-reserva-espacio.*` |
| Inscripción depende de cupos | RN-05 / RF-11 | Modelos `Actividad` e `InscripcionActividad`; estructura de datos y proceso diseñados | **Implementado parcialmente:** flujo de inscripción y control funcional de cupos pendientes | `actividades/models.py`; `docs/diagramas/05-proceso-actividad-cupos.*` |
| Publicar noticias y avisos | RF-13 | Modelos `Noticia` y `Aviso`, migraciones y administración | **Implementado parcialmente:** gestión de datos disponible; publicación para usuarios finales pendiente | `comunicaciones/models.py`; `comunicaciones/admin.py` |
| Notificar por WhatsApp | Propuesta APT | Integración considerada dentro del alcance del proyecto | **Pendiente** | No existe integración funcional actual |

---

## 3. Trazabilidad de seguridad y acceso

| Necesidad / regla | Requisito | Implementación actual | Estado | Evidencia técnica |
|---|---|---|---|---|
| Proteger acceso administrativo | RS-01 | Autenticación Django y protección del panel administrativo | **Implementado y probado** | `usuarios/tests.py`; `config/urls.py` |
| Proteger áreas privadas | RS-01 | Login obligatorio para paneles y vistas protegidas | **Implementado y probado** | `usuarios/views.py`; `usuarios/tests.py` |
| Controlar permisos según usuario y rol | RN-01 / RN-02 | Funciones y decoradores centralizados de autorización | **Implementado y probado** | `usuarios/permisos.py`; `usuarios/test_permisos.py` |
| Evitar acceso a información ajena | Regla de seguridad | Consultas filtradas por el vecino autenticado | **Implementado y probado** en Proyectos y Certificados | `proyectos/views.py`; `certificados/views.py`; pruebas automatizadas |
| Proteger secretos de configuración | RS-05 | Variables de entorno; `.env` excluido del repositorio y de la imagen Docker | **Implementado** | `.gitignore`; `.dockerignore`; `.env.example`; `config/settings.py` |
| Proteger operaciones que modifican estado | Regla de seguridad | Operaciones sensibles mediante POST y validación del estado previo | **Implementado y probado** | `proyectos/views.py`; `certificados/views.py`; pruebas automatizadas |

---

## 4. Trazabilidad técnica solicitada durante Capstone

| Elemento | Implementación actual | Estado | Evidencia |
|---|---|---|---|
| Arquitectura del sistema | Monolito modular Django conectado mediante ORM a PostgreSQL | **Implementada y documentada con Docker Compose** | `config/`; aplicaciones Django; `docs/diagramas/01-arquitectura-sut.*` |
| Modelo de datos | Modelos Django, migraciones y tablas PostgreSQL | **Implementado** | `models.py`; `migrations/`; `docs/diagramas/02-modelo-datos-sut.*` |
| Diagramas UML/BPM mínimos | Procesos de Proyectos, Reservas y Actividades documentados | **Disponibles** | `docs/diagramas/03-*`; `04-*`; `05-*` |
| Dockerización | Django y PostgreSQL ejecutados mediante Docker Compose | **Implementado y verificado** | `Dockerfile`; `compose.yml`; `.dockerignore` |
| Requisitos no funcionales | Seguridad, mantenibilidad, reproducibilidad, integridad, trazabilidad y disponibilidad de demostración | **Documentados según estado verificable** | `docs/especificaciones/especificaciones-tecnicas.md` |
| Pruebas automatizadas | Suite Django para autenticación, autorización, proyectos y certificados | **Implementado y verificado: 41/41** | `docs/pruebas/pruebas.md`; archivos de tests |
| Plan formal de pruebas | Plantilla entregada por el docente | **Completado para la Entrega 2.1; sujeto a actualización durante la Entrega 2.2** | `docs/pruebas/Plan_de_Pruebas_SUT_v0.1.xlsx` |
| Control de versiones | Desarrollo versionado mediante Git/GitHub | **Implementado** | historial Git y repositorio |
| Gestión del trabajo | Scrum apoyado mediante Jira | **Implementado y sincronizado hasta la Entrega 2.1; el nuevo avance se gestionará durante la Evaluación 3 / Entrega 2.2** | tablero Jira |

---

## 5. Cobertura actual

Los flujos con mayor nivel de madurez actualmente son:

### Autenticación y autorización

`Usuario → Login → Panel → Permiso → Recurso`

Estado:

**Implementado y probado.**

### Proyectos vecinales

`Miembro de junta → Postular → Pendiente → Directiva → Aprobar/Rechazar → Notificación`

Estado:

**Implementado y probado.**

### Certificados

`Vecino → Solicitar → Pendiente → Directiva → Aprobar/Rechazar → Emitir`

Estado:

**Implementado y probado.**

---

## 6. Funcionalidades todavía parciales o pendientes

Actualmente permanecen pendientes o parcialmente implementadas:

- registro/autogestión de vecinos desde interfaz de usuario;
- calendario y flujo de reservas;
- validación de disponibilidad de espacios;
- actividades e inscripciones;
- control funcional de cupos;
- publicación de noticias y avisos para usuarios finales;
- certificado descargable en formato documental/PDF;
- SMTP externo;
- integración WhatsApp;
- pruebas End to End mediante navegador.

Estas funcionalidades no deben presentarse como terminadas hasta contar con implementación y evidencia verificable.

---

## 7. Regla de trazabilidad del proyecto

Para considerar una funcionalidad completamente respaldada se busca mantener la siguiente cadena:

`Requisito → Jira → Implementación → Prueba → Commit → Evidencia → Documentación`

Por esta razón se distingue siempre entre:

`Diseñado ≠ Implementado ≠ Probado ≠ Evidenciado`

La matriz deberá actualizarse conforme se incorporen nuevos incrementos al sistema.