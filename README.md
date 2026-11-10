# Sistema Unidad Territorial · SUT

Sistema web desarrollado como proyecto Capstone de Ingeniería en Informática para apoyar la gestión administrativa y comunitaria de una junta de vecinos.

## Objetivo

Centralizar procesos habituales de una unidad territorial en una plataforma web simple, trazable y utilizable por vecinos y personal autorizado.

El SUT permite gestionar vecinos, certificados, proyectos, reservas, actividades y comunicaciones mediante una aplicación web responsiva conectada a PostgreSQL.

---

## Estado actual

La versión **SUT v1.0** se encuentra funcionalmente cerrada.

```text
Django                 6.1.3
PostgreSQL             18
Aplicaciones Django    7
Pruebas                133/133
Migraciones            15
E2E crítico            verificado
Escritorio             verificado
Dispositivo móvil      verificado
SMTP                    verificado
PDF certificados       verificado
```

Se mantiene un **Feature Freeze**. Sólo se realizarán correcciones que afecten la entrega, demostración, defensa o integridad funcional.

---

## Funcionalidades

### Vecinos

- registro de usuarios;
- perfil de vecino;
- edición de datos personales;
- gestión administrativa;
- incorporación y retiro como miembro de junta;
- control de permisos desde el servidor.

### Proyectos vecinales

```text
Miembro de junta
        ↓
Postulación
        ↓
Revisión
        ↓
Aprobación / Rechazo
        ↓
Notificación por correo
```

Incluye:

- postulación exclusiva para miembros;
- revisión por Directiva o personal autorizado;
- protección contra doble resolución;
- restricciones de estado;
- notificación HTML por correo;
- tolerancia a fallos SMTP sin revertir la resolución.

### Certificados de residencia

```text
Vecino
   ↓
Solicitud
   ↓
Revisión
   ↓
Aprobación / Rechazo
   ↓
Emisión
   ↓
PDF + correo
```

Incluye:

- control de solicitudes activas;
- aprobación, rechazo y emisión;
- protección contra doble resolución y emisión;
- snapshot de datos del vecino;
- generación y descarga privada del PDF;
- envío del certificado como adjunto por correo.

### Reservas

- reserva de espacios;
- calendario mensual;
- validación de fechas y horarios;
- detección de solapamientos;
- administración de espacios;
- protección frente a reservas concurrentes.

### Actividades

Para vecinos:

- consulta de actividades;
- inscripción;
- control de cupos;
- prevención de inscripciones duplicadas.

Para Directiva y personal autorizado:

- creación;
- edición;
- gestión de fechas y cupos;
- consulta de inscritos;
- eliminación cuando corresponde.

### Comunicaciones

- noticias;
- avisos;
- consulta pública;
- creación, edición y eliminación por usuarios autorizados;
- avisos destacados;
- interfaz responsiva.

---

## Roles

El sistema diferencia entre:

- vecino;
- miembro de junta;
- Directiva;
- personal autorizado;
- superusuario.

La autorización se valida del lado del servidor mediante reglas centralizadas.

---

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

Aplicaciones:

```text
usuarios
vecinos
proyectos
certificados
reservas
actividades
comunicaciones
```

El entorno se ejecuta mediante Docker Compose y PostgreSQL utiliza un volumen persistente.

---

## Tecnologías

- Python 3.14
- Django 6.1.3
- PostgreSQL 18
- Django ORM
- Django Templates
- Bootstrap 5.3.3
- ReportLab
- Docker
- Docker Compose

Gestión y trazabilidad:

- Git
- GitHub
- Jira

---

## Ejecución

Crear `.env` tomando `.env.example` como referencia.

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

---

## Pruebas

Ejecutar la suite:

```bash
docker compose exec -T web python manage.py test --verbosity 1
```

Último resultado:

```text
Found 133 test(s).
Ran 133 tests
OK
```

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

También se realizaron recorridos End to End sobre los flujos críticos y validaciones en escritorio y dispositivo móvil.

---

## Calidad y seguridad

El proyecto incorpora:

- protección CSRF;
- autorización del lado del servidor;
- aislamiento de información por usuario;
- restricciones de integridad en PostgreSQL;
- transacciones atómicas;
- `select_for_update()` en operaciones sensibles;
- escape automático mediante Django Templates;
- secretos fuera del repositorio;
- `.env` excluido de Git;
- contenedor web sin privilegios root;
- protección de descargas privadas.

Último checkpoint técnico:

```text
Django check            OK
133/133 pruebas         OK
Migraciones pendientes  ninguna
Docker Compose          OK
PostgreSQL              healthy
Aplicación Django       healthy
```

El entorno actual está orientado a desarrollo y demostración académica, no a despliegue productivo.

---

## Documentación

La documentación se mantiene en:

```text
docs/
├── cierre/
├── control/
├── diagramas/
├── especificaciones/
├── evidencias/
└── pruebas/
```

Incluye arquitectura, especificaciones técnicas, trazabilidad, pruebas, evidencias y documentación de cierre.

Los documentos históricos se conservan como registro de la evolución del proyecto y no representan necesariamente el estado técnico actual.

---

## Alcance de v1.0

La versión v1.0 incluye:

- gestión de vecinos;
- certificados de residencia;
- proyectos vecinales;
- reservas;
- actividades;
- noticias y avisos;
- control de acceso por roles;
- notificaciones por correo;
- generación de certificados PDF;
- interfaz web responsiva;
- persistencia mediante PostgreSQL.

La propuesta contempla comunicación mediante aviso, correo y/o WhatsApp.

La implementación actual utiliza:

```text
Avisos dentro del sistema
+
Correo electrónico
```

La integración directa con WhatsApp no forma parte de la versión v1.0.