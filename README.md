# Sistema Unidad Territorial — SUT

Proyecto Capstone de Ingeniería en Informática orientado a apoyar la gestión administrativa y comunitaria de una junta de vecinos.

## Objetivo

Mejorar la gestión de la unidad territorial de una junta de vecinos.

## Estado actual

El proyecto se encuentra en desarrollo incremental mediante Scrum.

La Entrega 2.1 consolidó una base funcional verificable con autenticación, autorización, proyectos vecinales, certificados de residencia, PostgreSQL, Docker Compose y pruebas automatizadas.

La Entrega 2.2 continúa el desarrollo sobre esta base, priorizando los flujos funcionales pendientes, la trazabilidad, las pruebas y las evidencias necesarias para demostrar el producto.

## Funcionalidades implementadas

### Infraestructura

- Django 6.1.
- PostgreSQL 18.
- Configuración mediante variables de entorno.
- Migraciones Django.
- Docker Compose.
- Contenedor `sut-web` para Django.
- Contenedor `sut-postgres` para PostgreSQL.
- Healthchecks para aplicación y base de datos.
- Migraciones automáticas al iniciar el servicio web.

### Identidad y autorización

- Login y logout.
- Panel privado.
- Modelo de roles.
- Perfil `Vecino`.
- Distinción de miembro de junta.
- Personal autorizado / Directiva.
- Permisos centralizados.
- Restricciones de acceso verificadas mediante pruebas automatizadas.

### Proyectos vecinales

Flujo implementado:

`Miembro de junta → Postular → Pendiente → Revisión → Aprobar/Rechazar → Notificación`

Incluye:

- postulación exclusiva para miembros de junta;
- estado inicial `PENDIENTE`;
- listado de proyectos propios;
- protección para evitar visualizar proyectos ajenos;
- revisión por personal autorizado;
- aprobación y rechazo;
- protección contra doble resolución;
- protección contra modificación manual del estado;
- generación de notificación por correo mediante Django.

### Certificados de residencia

Flujo implementado:

`Vecino → Solicitar → Pendiente → Revisión → Aprobar/Rechazar → Emitir`

Incluye:

- solicitud por vecinos autenticados;
- estado inicial `PENDIENTE`;
- seguimiento de solicitudes propias;
- protección para evitar visualizar solicitudes ajenas;
- revisión por personal autorizado;
- aprobación y rechazo;
- emisión lógica del certificado;
- estado `EMITIDA`;
- protección contra emisión de solicitudes rechazadas;
- protección contra emisión duplicada.

La emisión actual corresponde al registro del certificado dentro del sistema.

La generación de un archivo o PDF descargable permanece pendiente.

## Pruebas automatizadas

El baseline de inicio de la Entrega 2.2 posee:

**41 pruebas automatizadas aprobadas.**

La suite incluye pruebas de:

- autenticación;
- autorización;
- acceso anónimo;
- permisos por rol;
- miembros de junta;
- aislamiento de información entre usuarios;
- creación de proyectos;
- manipulación de estados;
- aprobación y rechazo de proyectos;
- notificaciones por correo;
- solicitud de certificados;
- aprobación y rechazo de certificados;
- emisión de certificados;
- operaciones duplicadas;
- reglas de negocio.

Resultado verificado:

```text
41 pruebas ejecutadas
41 aprobadas
0 fallidas
```

La suite fue verificada dentro del contenedor Docker de Django.

## Stack tecnológico

- Python 3.14
- Django 6.1
- PostgreSQL 18
- Django ORM
- Django Templates
- Bootstrap
- Docker
- Docker Compose
- Git
- GitHub
- Jira

## Arquitectura

El SUT utiliza una arquitectura web monolítica modular basada en aplicaciones Django.

Flujo general:

```text
Navegador
    ↓
Django
    ↓
Django ORM
    ↓
PostgreSQL
```

En el entorno Docker:

```text
Navegador
    ↓
localhost:8000
    ↓
sut-web
    ↓
db:5432
    ↓
sut-postgres
```

El proyecto está organizado en siete aplicaciones Django:

- `usuarios`
- `vecinos`
- `proyectos`
- `certificados`
- `reservas`
- `actividades`
- `comunicaciones`

## Docker

El sistema puede ejecutarse mediante Docker Compose.

Construir y levantar los servicios:

```bash
docker compose up -d --build
```

Verificar estado:

```bash
docker compose ps
```

Servicios esperados:

```text
sut-web        healthy
sut-postgres   healthy
```

La aplicación queda disponible en:

```text
http://127.0.0.1:8000/
```

### Ejecutar pruebas dentro de Docker

```bash
docker compose exec -T web python manage.py test --verbosity 1
```

Resultado verificado al inicio de la Entrega 2.2:

```text
Found 41 test(s).
.........................................
OK
```

## Ejecución local

Con el entorno virtual activo:

```bash
python manage.py runserver
```

Ejecutar pruebas:

```bash
python manage.py test
```

## Seguridad

Actualmente se utilizan:

- variables de entorno para configuración sensible;
- exclusión de `.env` mediante `.gitignore`;
- exclusión de `.env` mediante `.dockerignore`;
- validadores de contraseña de Django;
- protección CSRF;
- middleware de autenticación;
- control de acceso del lado del servidor;
- permisos reutilizables;
- separación entre autenticación y autorización;
- filtrado de información según el usuario autenticado.

La configuración sensible utilizada para desarrollo se mantiene fuera del repositorio mediante variables de entorno.

## Correo

El SUT implementa actualmente la lógica de notificación de resolución de proyectos mediante Django.

Las pruebas automatizadas verifican:

- envío al destinatario correcto;
- correo de aprobación;
- correo de rechazo;
- ausencia de error cuando el usuario no posee email;
- prevención de notificaciones duplicadas.

Actualmente se utiliza un backend de desarrollo.

La integración con un servidor SMTP externo permanece pendiente.

## Estado por módulo

| Módulo | Estado |
|---|---|
| Autenticación | Implementado y probado |
| Autorización / RBAC | Implementado y probado |
| Vecinos | Base de datos y perfiles implementados; flujo de usuario pendiente |
| Proyectos vecinales | Flujo principal implementado y probado |
| Certificados | Flujo principal implementado y probado |
| PostgreSQL | Implementado |
| Docker Compose | Implementado y verificado |
| Pruebas automatizadas | 41 aprobadas |
| Reservas | Base de datos implementada; flujo funcional pendiente |
| Actividades | Base de datos implementada; flujo funcional pendiente |
| Comunicaciones | Base de datos implementada; publicación para usuario final pendiente |
| SMTP externo | Pendiente |
| WhatsApp | Pendiente |
| Certificado PDF descargable | Pendiente |
| Pruebas End to End mediante navegador | Pendientes |

## Diseñado / pendiente de implementación funcional

Actualmente permanecen pendientes o parcialmente desarrollados:

- registro/autogestión de vecinos desde interfaz;
- calendario y flujo de reservas;
- validación de disponibilidad de espacios;
- actividades e inscripciones;
- control funcional de cupos;
- noticias y avisos para usuarios finales;
- SMTP externo;
- integración WhatsApp;
- generación de certificado PDF descargable;
- pruebas End to End mediante navegador;
- refinamiento de interfaz.

Estas funcionalidades no deben presentarse como terminadas hasta contar con implementación y evidencia verificable.

## Documentación

El repositorio mantiene documentación organizada en:

```text
docs/
├── cierre/
├── control/
├── diagramas/
├── especificaciones/
├── evidencias/
└── pruebas/
```

### Diagramas

`docs/diagramas/`

Contiene:

- arquitectura del SUT;
- modelo de datos;
- proceso de proyectos vecinales;
- proceso de reservas;
- proceso de actividades y cupos.

Los diagramas correspondientes a funcionalidades aún pendientes representan diseño y no acreditan por sí solos una implementación funcional.

### Evidencias

`docs/evidencias/`

Contiene evidencias técnicas del proceso de desarrollo, incluyendo pruebas automatizadas, Docker, HTTP y recorridos funcionales de Proyectos y Certificados.

### Pruebas

`docs/pruebas/`

Documenta la estrategia, el plan y la ejecución de pruebas.

### Control y trazabilidad

`docs/control/`

Mantiene la relación entre necesidades, reglas, implementación, pruebas y evidencias.

La matriz de trazabilidad distingue entre funcionalidades diseñadas, implementadas, probadas y evidenciadas.

### Cierre y checkpoints

`docs/cierre/`

Mantiene documentación histórica de los principales checkpoints del proyecto.

Entre ellos:

- cierre de la versión v0.1;
- avance correspondiente a la Entrega 2.1;
- futuros documentos de cierre de la Entrega 2.2.

### Especificaciones técnicas

`docs/especificaciones/especificaciones-tecnicas.md`

Consolida arquitectura, tecnologías, alcance y requisitos no funcionales verificables.

## Metodología de desarrollo

El desarrollo se gestiona mediante Scrum apoyado por Jira.

Git y GitHub se utilizan para control de versiones y trazabilidad técnica.

El flujo de trabajo busca mantener la relación:

```text
Requisito
    ↓
Jira / Sprint
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

Los cambios se integran mediante incrementos funcionales verificables.

Como criterio de trazabilidad se mantiene la distinción:

```text
Diseñado
≠
Implementado
≠
Probado
≠
Evidenciado
```

## Baseline de inicio de la Entrega 2.2

Estado técnico verificado antes de iniciar nuevos incrementos:

```text
Django system check     OK
PostgreSQL              healthy
sut-web                 healthy
sut-postgres            healthy
HTTP                    200
Pruebas automatizadas   41/41
Rama principal          main
Commit base             edef585
Docker Compose          operativo
```

Este baseline constituye el punto de partida técnico de la Entrega 2.2.

## Próximos pasos

Durante la Entrega 2.2 se priorizarán las siguientes actividades:

1. consolidar la coherencia entre documentación, Jira, GitHub, código y evidencias;
2. definir y priorizar los incrementos funcionales pendientes según el alcance del proyecto;
3. implementar cada incremento junto con sus reglas de negocio y permisos;
4. ampliar las pruebas automatizadas y ejecutar pruebas funcionales de los nuevos flujos;
5. generar evidencia verificable de cada funcionalidad implementada;
6. actualizar Jira, trazabilidad y documentación conforme avance el desarrollo;
7. preparar la retrospectiva y la demostración final del producto.

La prioridad de los módulos pendientes se definirá según impacto funcional, riesgo para la entrega y capacidad de ser implementados, probados y defendidos correctamente.