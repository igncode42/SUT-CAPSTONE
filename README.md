# Sistema Unidad Territorial · SUT

Sistema web desarrollado como proyecto Capstone de Ingeniería en Informática para apoyar la gestión administrativa y comunitaria de una junta de vecinos.

## Objetivo

Centralizar procesos habituales de una unidad territorial en una plataforma web responsiva, trazable y respaldada por PostgreSQL.

SUT permite gestionar vecinos, proyectos, certificados, reservas, actividades y comunicaciones mediante distintos niveles de autorización.

---

## Estado

La versión **SUT v1.0** se encuentra funcionalmente cerrada.

```text
Django                 6.1.3
PostgreSQL             18
Aplicaciones Django    7
Pruebas                133/133
Migraciones            15
E2E manual             verificado
SMTP                    verificado
PDF certificados       verificado
Responsive              verificado
```

El proyecto se encuentra en **Feature Freeze**. Sólo se consideran correcciones que afecten entrega, demostración, defensa o integridad funcional.

---

## Funcionalidades

### Vecinos

- registro y perfil;
- edición de datos;
- gestión administrativa;
- membresía de junta;
- control de permisos desde servidor.

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
Correo
```

Incluye autorización por rol, protección contra doble resolución, estados controlados y tolerancia ante fallos SMTP.

### Certificados de residencia

```text
Vecino
   ↓
Solicitud
   ↓
Revisión
   ↓
Aprobación
   ↓
Emisión
   ↓
PDF + correo
```

Incluye control de solicitudes activas, snapshot de datos, prevención de doble emisión y acceso privado al documento.

### Reservas

- reserva de espacios;
- calendario mensual;
- validación de fechas y horarios;
- control de solapamientos;
- administración de espacios.

### Actividades

- consulta e inscripción;
- control de cupos y duplicados;
- creación y edición administrativa;
- consulta de inscritos;
- eliminación cuando corresponde.

### Comunicaciones

- noticias y avisos;
- consulta pública;
- gestión por usuarios autorizados;
- visualización responsiva.

---

## Roles

El sistema diferencia entre:

- vecino;
- miembro de junta;
- Directiva;
- personal autorizado;
- superusuario.

La autorización se valida en el servidor mediante reglas centralizadas.

---

## Arquitectura

SUT utiliza una arquitectura web monolítica modular basada en Django.

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
- Docker y Docker Compose
- Git / GitHub
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

Aplicación local:

```text
http://127.0.0.1:8000/
```

---

## Pruebas

Ejecutar la suite:

```bash
docker compose exec -T web python manage.py test --verbosity 1
```

Último resultado verificado:

```text
Found 133 test(s).
Ran 133 tests
OK
```

Los recorridos End to End manuales cubren los principales flujos de proyectos, certificados, reservas, actividades y comunicaciones.

La estrategia completa y el Plan de Pruebas se encuentran en `docs/pruebas/`.

---

## Calidad y seguridad

El proyecto incorpora:

- protección CSRF;
- autorización del lado del servidor;
- aislamiento de información;
- restricciones de integridad;
- transacciones atómicas;
- `select_for_update()` en operaciones sensibles;
- secretos fuera del repositorio;
- `.env` excluido de Git;
- descargas privadas protegidas;
- contenedor web sin privilegios root.

Verificaciones finales:

```text
Django check            OK
Pruebas                 133/133
Migraciones pendientes  ninguna
Gitleaks                 sin secretos detectados
pip-audit                sin vulnerabilidades conocidas
check --deploy           sin incidencias en perfil seguro simulado
```

El entorno actual está destinado a desarrollo y demostración académica, no a despliegue productivo.

---

## Documentación

```text
docs/
├── cierre/
├── control/
├── diagramas/
├── especificaciones/
├── evidencias/
└── pruebas/
```

La documentación incluye arquitectura, modelo de datos, UML/BPMN, especificaciones técnicas, trazabilidad, pruebas, evidencias y cierre del proyecto.

Las versiones históricas se conservan como registro de evolución y no representan necesariamente el estado técnico actual.

---

## Alcance de v1.0

La versión v1.0 implementa los procesos principales definidos para el proyecto.

Quedan fuera del alcance demostrado:

- integración directa con WhatsApp;
- pruebas End to End automatizadas mediante navegador;
- despliegue productivo en infraestructura externa;
- pruebas formales de carga o rendimiento.

La versión actual utiliza avisos dentro del sistema y correo electrónico para sus comunicaciones implementadas.