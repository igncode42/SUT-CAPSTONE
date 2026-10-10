# Sistema Unidad Territorial — SUT

Proyecto Capstone de Ingeniería en Informática orientado a apoyar la gestión administrativa y comunitaria de una junta de vecinos.

## Objetivo

Mejorar la gestión de la unidad territorial de una junta de vecinos.

## Estado actual

El proyecto se encuentra en desarrollo incremental mediante Scrum.

Actualmente existe una base funcional verificable con autenticación, autorización por roles, proyectos vecinales, certificados de residencia, PostgreSQL y ejecución mediante Docker Compose.

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

- Postulación exclusiva para miembros de junta.
- Estado inicial `PENDIENTE`.
- Listado de proyectos propios.
- Protección para evitar visualizar proyectos ajenos.
- Revisión por personal autorizado.
- Aprobación y rechazo.
- Protección contra doble resolución.
- Protección contra modificación manual del estado.
- Generación de notificación por correo mediante Django.

### Certificados de residencia

Flujo implementado:

`Vecino → Solicitar → Pendiente → Revisión → Aprobar/Rechazar → Emitir`

Incluye:

- Solicitud por vecinos autenticados.
- Estado inicial `PENDIENTE`.
- Seguimiento de solicitudes propias.
- Protección para evitar visualizar solicitudes ajenas.
- Revisión por personal autorizado.
- Aprobación y rechazo.
- Emisión lógica del certificado.
- Estado `EMITIDA`.
- Protección contra emisión de solicitudes rechazadas.
- Protección contra emisión duplicada.

## Pruebas automatizadas

Actualmente el SUT posee:

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

El checkpoint actual fue verificado dentro del contenedor Docker de Django.

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

Resultado actualmente verificado:

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
- control de acceso por servidor;
- permisos reutilizables;
- separación entre autenticación y autorización;
- filtrado de información según el usuario autenticado.

Los secretos reales no se almacenan en el repositorio.

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
| Autenticación | Implementado |
| Autorización / RBAC | Implementado |
| Vecinos | Base de datos y perfiles implementados |
| Proyectos vecinales | Flujo principal implementado |
| Certificados | Flujo principal implementado |
| PostgreSQL | Implementado |
| Docker Compose | Implementado |
| Pruebas automatizadas | 41 aprobadas |
| Reservas | Base de datos implementada; flujo pendiente |
| Actividades | Base de datos implementada; flujo pendiente |
| Comunicaciones | Base de datos implementada; interfaz final pendiente |
| SMTP externo | Pendiente |
| WhatsApp | Pendiente |
| Certificado PDF descargable | Pendiente |

## Diseñado / pendiente de implementación funcional

Actualmente permanecen pendientes o parcialmente desarrollados:

- calendario de reservas;
- validación de disponibilidad de espacios;
- actividades;
- inscripciones;
- control funcional de cupos;
- noticias y avisos para usuarios finales;
- SMTP externo;
- integración WhatsApp;
- generación de certificado PDF descargable;
- refinamiento de interfaz.

## Documentación

El repositorio mantiene documentación organizada en:

```text
docs/
├── closure/
├── control/
├── diagrams/
├── evidence/
├── technical/
└── testing/
```

### Diagramas

`docs/diagrams/`

Contiene:

- arquitectura del SUT;
- modelo de datos;
- proceso de proyectos vecinales;
- proceso de reservas;
- proceso de actividades y cupos.

### Evidencias

`docs/evidence/`

Contiene evidencias técnicas del proceso de desarrollo, incluyendo pruebas automatizadas, Docker/HTTP y recorridos funcionales de Proyectos y Certificados.

### Pruebas

`docs/testing/`

Documenta la estrategia y ejecución de pruebas.

### Control y trazabilidad

`docs/control/`

Mantiene la relación entre necesidades, reglas, implementación y evidencias.

### Avances

`docs/closure/`

Mantiene checkpoints documentales del desarrollo del proyecto.

### Especificaciones técnicas

`docs/technical/especificaciones-tecnicas.md`

Consolida arquitectura, tecnologías, alcance actual y requisitos no funcionales verificables.

## Metodología de desarrollo

El desarrollo actual se gestiona mediante Scrum apoyado por Jira.

Git y GitHub se utilizan para control de versiones y trazabilidad técnica.

El flujo de trabajo utilizado busca mantener la relación:

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
```

Los cambios se integran mediante incrementos funcionales verificables.

## Estado técnico verificado

Checkpoint actual:

```text
Django system check     OK
PostgreSQL              healthy
sut-web                 healthy
sut-postgres            healthy
HTTP                    200
Pruebas automatizadas   41/41
Rama principal          main
Docker Compose          operativo
```

## Próximos pasos

Para el cierre del checkpoint actual:

1. sincronizar Jira/Scrum con el estado real;
2. realizar commit y push del avance;
3. preparar la carpeta compartida solicitada;
4. grabar el video breve de demostración.

Los siguientes incrementos funcionales se priorizarán después de la retroalimentación docente. Entre ellos permanecen Reservas, Actividades, Comunicaciones para usuario final, certificado descargable y SMTP externo.
