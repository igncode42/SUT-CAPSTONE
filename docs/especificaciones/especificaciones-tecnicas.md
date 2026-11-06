# Especificaciones técnicas — Sistema Unidad Territorial

## 1. Objetivo

Documentar la arquitectura, tecnologías, requisitos y controles técnicos implementados en el Sistema Unidad Territorial (SUT) para la Entrega 2.2 de Capstone.

## 2. Alcance

El SUT es una aplicación web para apoyar la gestión administrativa y comunitaria de una junta de vecinos.

Actualmente permite gestionar:

- vecinos y membresía;
- proyectos vecinales;
- certificados de residencia;
- reservas de espacios;
- actividades y cupos;
- noticias y avisos;
- autenticación, roles y permisos.

El sistema utiliza PostgreSQL como base de datos y puede ejecutarse mediante Docker Compose.

## 3. Tecnologías

| Componente | Tecnología | Uso |
|---|---|---|
| Lenguaje | Python 3.14 | Lógica de aplicación |
| Framework | Django 6.1.3 | Aplicación web, ORM, autenticación y pruebas |
| Base de datos | PostgreSQL 18 | Persistencia |
| Interfaz | Django Templates + Bootstrap 5.3.3 | Interfaz web responsiva |
| Contenedores | Docker + Docker Compose | Entorno reproducible |
| Control de versiones | Git + GitHub | Historial y trazabilidad |
| Gestión | Jira + Scrum | Planificación y seguimiento |

## 4. Arquitectura

El proyecto utiliza una arquitectura web monolítica modular basada en aplicaciones Django.

```text
Interfaz web
    ↓
Django
    ↓
Aplicaciones
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

En Docker Compose:

```text
Navegador
    ↓
127.0.0.1:8000
    ↓
sut-web
    ↓
Django ORM
    ↓
sut-postgres
```

El contenedor web se ejecuta con un usuario sin privilegios de root.

Respaldo gráfico: `docs/diagramas/01-arquitectura-sut.svg`.

## 5. Requisitos funcionales

### RF-01 — Gestión de vecinos

El sistema permite:

- registrar nuevos vecinos;
- asociar un usuario con su perfil de vecino;
- gestionar vecinos desde perfiles autorizados;
- incorporar o retirar la condición de miembro de junta.

Los privilegios no pueden asignarse mediante el formulario público de registro.

### RF-02 — Proyectos vecinales

Flujo:

`Miembro → Postulación → Pendiente → Revisión → Aprobación/Rechazo`

Controles:

- sólo miembros de junta pueden postular;
- propietario y estado se asignan en servidor;
- sólo personal autorizado resuelve;
- una resolución no puede repetirse;
- los estados válidos están restringidos en PostgreSQL.

### RF-03 — Resolución por correo

La resolución de un proyecto puede notificarse al postulante mediante correo electrónico.

Se encuentra implementado:

- correo de aprobación;
- correo de rechazo;
- destinatario asociado al postulante;
- comportamiento ante usuario sin email;
- tolerancia ante fallo SMTP.

Una falla del servicio SMTP no revierte la resolución ya registrada.

La integración con un servidor SMTP externo fue validada mediante un recorrido funcional controlado.

### RF-04 — Certificados

Flujo:

`Vecino → Solicitud → Revisión → Aprobación/Rechazo → Emisión`

Controles:

- la solicitud pertenece al vecino autenticado;
- sólo existe una solicitud activa por vecino;
- sólo personal autorizado puede resolver;
- se evita la doble resolución y doble emisión;
- los estados válidos están restringidos en PostgreSQL;
- el certificado emitido conserva un snapshot de los datos del vecino.

### RF-05 — Reservas

El sistema permite:

- reservar espacios activos;
- consultar reservas propias;
- visualizar un calendario mensual;
- rechazar fechas pasadas;
- exigir hora de inicio menor a hora de término;
- detectar horarios solapados;
- excluir reservas canceladas de la disponibilidad.

La operación utiliza transacción y bloqueo del espacio para volver a comprobar su estado y los solapamientos antes de guardar.

### RF-06 — Actividades

El sistema permite:

- consultar actividades disponibles;
- inscribirse en actividades vigentes;
- impedir inscripciones duplicadas;
- controlar el cupo máximo.

La inscripción utiliza transacción y bloqueo de la actividad para proteger el control de cupos.

### RF-07 — Comunicaciones

El sistema permite:

- publicar noticias;
- publicar avisos;
- consultar comunicaciones;
- restringir la publicación a perfiles autorizados.

El contenido se presenta utilizando el escape automático de Django Templates.

### RF-08 — Autenticación y autorización

El sistema diferencia:

- usuario autenticado;
- vecino;
- miembro de junta;
- Directiva;
- personal autorizado;
- superusuario.

Los permisos funcionales se validan del lado del servidor mediante reglas centralizadas.

## 6. Requisitos no funcionales

| ID | Requisito | Estado / respaldo |
|---|---|---|
| RNF-01 | Mantener configuración sensible fuera del repositorio | Variables de entorno, `.gitignore`, `.dockerignore` y `.env.example` |
| RNF-02 | Controlar acceso según autenticación y autorización | Permisos centralizados y pruebas automáticas |
| RNF-03 | Mantener separación modular por dominio | 7 aplicaciones Django |
| RNF-04 | Proporcionar persistencia relacional | PostgreSQL 18 + Django ORM |
| RNF-05 | Mantener integridad de datos | Validaciones, transacciones y constraints PostgreSQL |
| RNF-06 | Reducir condiciones de carrera en operaciones críticas | `transaction.atomic()` y `select_for_update()` |
| RNF-07 | Permitir reproducción del entorno | Dockerfile + Docker Compose |
| RNF-08 | Proporcionar interfaz adaptable | Django Templates + Bootstrap |
| RNF-09 | Mantener trazabilidad del desarrollo | Git, GitHub, Jira, pruebas y documentación |
| RNF-10 | Ejecutar el proceso web sin privilegios root | Usuario `sut` en el contenedor web |

No se declaran métricas productivas de carga, rendimiento o disponibilidad porque no fueron medidas formalmente.

## 7. Integridad y seguridad

El sistema incorpora controles en distintas capas:

```text
Formulario
    ↓
Vista / autorización
    ↓
Reglas de negocio
    ↓
Transacción
    ↓
Restricciones PostgreSQL
```

Entre los controles implementados se encuentran:

- protección CSRF;
- validación de permisos en servidor;
- aislamiento de información por usuario;
- estados válidos mediante constraints;
- prevención de operaciones duplicadas;
- bloqueo de filas en operaciones sensibles;
- secretos fuera del código fuente;
- escape de contenido en templates;
- contenedor web ejecutado sin privilegios root.

La configuración permite habilitar medidas para un entorno HTTPS, como cookies seguras, redirección SSL y HSTS.

Esto representa preparación configurable para despliegue seguro y no un despliegue productivo actualmente demostrado.

## 8. Pruebas

La suite automática actual contiene:

```text
Usuarios          16
Vecinos           13
Proyectos         19
Certificados      20
Reservas          13
Actividades        7
Comunicaciones     9
────────────────────
Total             97
```

Último resultado verificado:

```text
Found 97 test(s).
Ran 97 tests
OK
```

También se realizaron recorridos End to End manuales para los flujos críticos de Proyectos y Certificados.

El detalle se mantiene en `docs/pruebas/`.

## 9. Ejecución

Crear `.env` tomando `.env.example` como referencia.

Levantar el entorno:

```bash
docker compose up -d --build
```

Verificar Django:

```bash
docker compose exec -T web python manage.py check
```

Ejecutar pruebas:

```bash
docker compose exec -T web python manage.py test --verbosity 1
```

Verificar cambios pendientes de modelos:

```bash
docker compose exec -T web python manage.py makemigrations --check --dry-run
```

Último checkpoint:

```text
Django check          OK
Pruebas               97/97
Migraciones nuevas    No changes detected
Backend               Congelado
```

## 10. Límites actuales

No forman parte de la implementación demostrada:

- integración con WhatsApp;
- generación de certificado como archivo PDF;
- pruebas End to End automatizadas mediante navegador;
- despliegue productivo en infraestructura externa;
- pruebas formales de carga o rendimiento.

Estas capacidades no se presentan como implementadas en la Entrega 2.2.