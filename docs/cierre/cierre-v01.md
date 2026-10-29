# Cierre de avance v0.1 — Sistema Unidad Territorial

**Estado del documento:** Histórico  
**Versión:** v0.1  
**Uso:** Evidencia del estado inicial del proyecto. No representa el estado vigente de la Entrega 2.2.

---

## Estado del proyecto

SUT v0.1 constituye una base técnica y documental verificable para continuar el desarrollo incremental.

Esta versión no se presenta como un producto terminado ni como una implementación completa de todos los procesos definidos.

El contenido de este documento debe interpretarse según el estado que tenía el sistema al cierre de la versión v0.1.

---

## Diseñado / documentado

- Fundamentación, problemática, solución, objetivos, alcance y factibilidad.
- Procesos principales de proyectos vecinales, reservas y actividades con cupos.
- Requisitos funcionales y no funcionales, reglas de negocio e historias de usuario.
- Product Backlog y criterios de priorización.
- Arquitectura del sistema, incluido el componente de correo como diseño.
- Modelo conceptual de datos.
- Stack tecnológico y organización modular de la solución.
- Matriz de trazabilidad, documentación de pruebas y cierre del avance.

Los diagramas de procesos expresan el comportamiento esperado del sistema y no acreditan flujos completos implementados.

---

## Implementado / verificado

- Proyecto Django inicial con las siete aplicaciones definidas: `usuarios`, `vecinos`, `certificados`, `proyectos`, `reservas`, `actividades` y `comunicaciones`.
- Modelos Django, migraciones y tablas asociadas en PostgreSQL.
- Usuario PostgreSQL dedicado y configuración de conexión mediante variables de entorno.
- Interfaz web inicial con Django Templates y Bootstrap.
- Registro de modelos en Django Admin y autenticación administrativa.
- Exclusión de `.env`, entornos virtuales, cachés y archivos compilados mediante `.gitignore`.
- Dos pruebas automatizadas iniciales ejecutadas y documentadas.
- Evidencias técnicas organizadas y numeradas para la versión v0.1.

---

## Pendiente al cierre de v0.1

- Completar los flujos funcionales para usuarios finales.
- Aplicar permisos específicos y validaciones finas según rol.
- Implementar notificaciones funcionales por correo y WhatsApp.
- Implementar calendario, disponibilidad y validaciones de reservas.
- Implementar el control funcional de cupos e inscripciones.
- Completar la solicitud y emisión funcional de certificados.
- Completar la publicación de comunicaciones para usuarios finales.
- Incorporar reglas de negocio adicionales y ampliar la cobertura de pruebas.
- Refinar la interfaz de usuario.
- Completar la planificación temporal y la presentación correspondiente a las siguientes etapas.

> **Nota histórica:** durante esta etapa se consideró utilizar Carta Gantt como parte de la planificación. En iteraciones posteriores la gestión del proyecto se organizó mediante Scrum y Jira de acuerdo con las indicaciones docentes vigentes.

---

## Conclusión del avance

La versión v0.1 demuestra la factibilidad técnica de la arquitectura, la persistencia en PostgreSQL, la administración inicial, la configuración segura y dos comportamientos básicos verificados.

El desarrollo pendiente correspondía principalmente a flujos de usuario, reglas de negocio y permisos. Por ello, esta versión debía defenderse como una base técnica coherente y documentada para las siguientes iteraciones.

Los avances posteriores del proyecto se documentan de forma independiente y no modifican retrospectivamente el estado registrado en esta versión.