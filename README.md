# Sistema Unidad Territorial — SUT

Sistema web desarrollado como proyecto Capstone de Ingeniería en Informática para apoyar la gestión administrativa y comunitaria de una junta de vecinos.

## Objetivo

Centralizar procesos habituales de una unidad territorial en una plataforma web simple, trazable y utilizable por vecinos y personal autorizado.

## Estado actual

El SUT se encuentra funcionalmente cerrado para la Entrega 2.2.

Estado técnico verificado:

- Django 6.1.3.
- PostgreSQL 18.
- Docker Compose.
- 7 aplicaciones Django.
- 97 pruebas automatizadas aprobadas.
- 15 migraciones de aplicación.
- 22 templates HTML.
- configuración sensible mediante variables de entorno.
- backend e integridad funcional congelados salvo corrección de errores.

## Funcionalidades

### Vecinos

- registro de usuarios y perfil de vecino;
- gestión interna de vecinos;
- incorporación y retiro como miembro de junta;
- control de privilegios desde servidor.

### Proyectos vecinales

Flujo principal:

`Miembro de junta → Postulación → Revisión → Aprobación/Rechazo → Notificación`

Incluye:

- postulación exclusiva para miembros;
- revisión por Directiva o personal autorizado;
- protección contra doble resolución;
- restricciones de estado en PostgreSQL;
- notificación de resolución por correo;
- tolerancia a fallos del servicio SMTP sin revertir la decisión registrada.

### Certificados de residencia

Flujo principal:

`Vecino → Solicitud → Revisión → Aprobación/Rechazo → Emisión`

Incluye:

- una solicitud activa por vecino;
- revisión por personal autorizado;
- protección contra doble resolución y doble emisión;
- snapshot de los datos del vecino al emitir el certificado;
- restricciones de integridad en base de datos.

### Reservas

- reserva de espacios;
- calendario mensual;
- validación de fechas y horarios;
- detección de solapamientos;
- espacios activos;
- protección transaccional contra reservas concurrentes mediante bloqueo del espacio;
- restricciones de estado y horario en PostgreSQL.

### Actividades

- publicación de actividades;
- inscripción de vecinos;
- control de cupos;
- prevención de inscripciones duplicadas;
- bloqueo transaccional durante la inscripción;
- restricción de cupo mínimo en base de datos.

### Comunicaciones

- publicación de noticias;
- publicación de avisos;
- consulta pública;
- publicación restringida a usuarios autorizados;
- escape de contenido mediante Django Templates.

## Roles y autorización

El sistema diferencia entre:

- usuario autenticado;
- vecino;
- miembro de junta;
- Directiva;
- personal autorizado;
- superusuario.

Los permisos funcionales se validan del lado del servidor mediante reglas centralizadas.

La autenticación y la autorización se tratan como responsabilidades independientes.

## Arquitectura

El SUT utiliza una arquitectura web monolítica modular basada en Django.

```text
Navegador
    ↓
Django
    ↓
Django ORM
    ↓
PostgreSQL
```

Aplicaciones principales:

```text
usuarios
vecinos
proyectos
certificados
reservas
actividades
comunicaciones
```

El entorno de desarrollo y demostración se ejecuta mediante Docker Compose:

```text
Navegador
    ↓
127.0.0.1:8000
    ↓
sut-web
    ↓
PostgreSQL
```

## Stack

- Python 3.14
- Django 6.1.3
- PostgreSQL 18
- Django ORM
- Django Templates
- Bootstrap 5
- Docker
- Docker Compose
- Git
- GitHub
- Jira

## Ejecución con Docker

Crear un archivo `.env` a partir de `.env.example` y completar la configuración requerida.

Luego:

```bash
docker compose up -d --build
```

Verificar servicios:

```bash
docker compose ps
```

Aplicación:

```text
http://127.0.0.1:8000/
```

## Pruebas

Ejecutar la suite completa:

```bash
docker compose exec -T web python manage.py test --verbosity 1
```

Resultado del último checkpoint técnico:

```text
Found 97 test(s).
Ran 97 tests
OK
```

Distribución actual:

| Aplicación | Pruebas |
|---|---:|
| Usuarios | 16 |
| Vecinos | 13 |
| Proyectos | 19 |
| Certificados | 20 |
| Reservas | 13 |
| Actividades | 7 |
| Comunicaciones | 9 |
| **Total** | **97** |

También se ejecutaron manualmente recorridos End to End de los flujos críticos de Proyectos y Certificados.

## Calidad y seguridad

El proyecto incorpora:

- protección CSRF;
- autorización del lado del servidor;
- aislamiento de información por usuario;
- restricciones de integridad en PostgreSQL;
- transacciones y bloqueos `select_for_update()` en operaciones sensibles;
- escape de contenido en templates;
- secretos fuera del repositorio;
- contenedor web ejecutado con usuario no root;
- configuración de seguridad parametrizable para entornos HTTPS.

Durante el hardening se verificó además:

```text
Django system check     OK
97/97 pruebas           OK
makemigrations --check  sin cambios
check --deploy          sin observaciones bajo perfil simulado
Gitleaks                sin filtraciones detectadas
pip-audit               sin vulnerabilidades conocidas detectadas
```

El entorno Docker actual está orientado a desarrollo y demostración; no representa por sí solo un despliegue productivo.

## Documentación

La documentación técnica se mantiene en:

```text
docs/
├── cierre/
├── control/
├── diagramas/
├── especificaciones/
├── evidencias/
└── pruebas/
```

Incluye:

- arquitectura;
- modelo de datos;
- procesos principales;
- especificaciones técnicas;
- trazabilidad;
- estrategia y plan de pruebas;
- evidencias del desarrollo;
- checkpoints y documentación de cierre.

Los documentos históricos se conservan como evidencia de la evolución del proyecto y no representan necesariamente el estado técnico actual.

## Metodología y trazabilidad

El desarrollo se ha gestionado de forma incremental mediante Scrum, utilizando Jira para seguimiento y Git/GitHub para control de versiones.

El criterio de trabajo mantiene la relación:

```text
Requisito
    ↓
Planificación
    ↓
Implementación
    ↓
Prueba
    ↓
Commit
    ↓
Evidencia
```

Durante el proyecto se distingue explícitamente entre:

```text
Diseñado
≠
Implementado
≠
Probado
≠
Demostrado
```

## Checkpoint técnico

Último cierre funcional:

```text
Rama                 main
Commit                ecfde54
Pruebas               97/97
Django check          OK
Migraciones nuevas    no pendientes
Backend               congelado
```

A partir de este punto, el trabajo se concentra en documentación, evidencias, experiencia de usuario, presentación y preparación de la demostración final.