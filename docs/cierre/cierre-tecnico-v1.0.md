# Cierre técnico — Sistema Unidad Territorial v1.0

## Estado

La versión **v1.0** corresponde al cierre técnico del Sistema Unidad Territorial (SUT).

El sistema se encuentra implementado, validado y respaldado mediante pruebas, documentación y evidencias de la Entrega 2.2.

## Diseñado y documentado

- arquitectura y modelo de datos;
- requisitos funcionales y no funcionales;
- roles, permisos y reglas de negocio;
- flujos principales, UML y BPMN;
- plan de pruebas y documentación técnica.

## Implementado

- autenticación, usuarios y vecinos;
- proyectos vecinales;
- certificados con PDF y correo;
- reservas de espacios;
- actividades e inscripciones;
- noticias y avisos;
- autorización por roles;
- PostgreSQL y Docker Compose.

## Validado

- **133 pruebas automatizadas aprobadas**;
- recorridos End to End manuales de los principales flujos;
- permisos, reglas de negocio e integridad de datos;
- Django check y ausencia de migraciones pendientes;
- controles de seguridad y calidad;
- funcionamiento en escritorio y móvil.

El cierre se encuentra respaldado por las evidencias conservadas en `docs/evidencias/fase-2.2/`.

## Fuera del alcance

- integración directa con WhatsApp;
- End to End automatizado mediante navegador;
- despliegue productivo en infraestructura externa;
- pruebas formales de carga o rendimiento.

## Cierre

SUT v1.0 cubre las principales funcionalidades definidas para el proyecto y cuenta con respaldo técnico, pruebas, evidencias y documentación coherente con su estado implementado.