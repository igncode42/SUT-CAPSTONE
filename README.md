# Sistema Unidad Territorial — SUT

Proyecto Capstone de Ingeniería en Informática orientado a apoyar la gestión administrativa y comunitaria de una junta de vecinos.

## Objetivo

Mejorar la gestión de la unidad territorial mediante una solución digital centralizada, trazable y acorde con los procesos definidos para la organización vecinal.

## Estado de la versión v0.1

### Diseñado

- Gestión de usuarios, roles y vecinos.
- Solicitud y emisión de certificados de residencia.
- Proyectos vecinales y su proceso de aprobación.
- Reservas de espacios comunitarios.
- Actividades, inscripciones y control de cupos.
- Noticias y avisos.
- Arquitectura del sistema, modelo conceptual de datos y procesos de negocio.
- Requisitos, reglas de negocio, historias de usuario, Product Backlog y trazabilidad.
- Componente de correo como parte de la arquitectura propuesta.

### Implementado

- Proyecto Django organizado en siete aplicaciones: `usuarios`, `vecinos`, `certificados`, `proyectos`, `reservas`, `actividades` y `comunicaciones`.
- Modelos Django, migraciones y tablas asociadas en PostgreSQL.
- Interfaz web inicial con Django Templates y Bootstrap.
- Django Admin y autenticación para el acceso administrativo.
- Configuración mediante variables de entorno y exclusión de secretos con `.gitignore`.
- Dos pruebas automatizadas iniciales documentadas en `docs/testing/pruebas.md`.
- Documentación técnica, diagramas y evidencias de la base v0.1.

### Pendiente

- Flujos funcionales completos para usuarios finales.
- Permisos específicos y validaciones finas según rol.
- Envío funcional de notificaciones por correo y WhatsApp.
- Calendario y validación funcional de disponibilidad para reservas.
- Control funcional de cupos e inscripciones.
- Reglas de negocio adicionales, mayor cobertura de pruebas y refinamiento de la interfaz.
- Carta Gantt con fechas oficiales y presentación final.

## Stack tecnológico

- Python
- Django
- PostgreSQL
- Django ORM
- Django Templates
- Bootstrap
- Git / GitHub

## Arquitectura

Aplicación web responsiva basada en un monolito modular Django conectado a PostgreSQL. Los componentes de notificación representados en la arquitectura corresponden al diseño y no a una integración funcional de la versión v0.1.

El modelo de datos documentado es conceptual. Los diagramas de procesos describen el diseño previsto del sistema y no acreditan por sí solos flujos de usuario implementados.

## Documentación

- `docs/diagrams/`: arquitectura, modelo conceptual de datos y procesos diseñados.
- `docs/evidence/`: evidencias de implementación y verificación de la versión v0.1.
- `docs/testing/`: pruebas ejecutadas y pruebas futuras.
- `docs/control/`: matriz de trazabilidad y estado de requisitos.
- `docs/closure/`: cierre y pendientes del avance v0.1.
