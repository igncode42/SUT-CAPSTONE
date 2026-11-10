# Especificaciones técnicas · Sistema Unidad Territorial

## 1. Objetivo

Documentar la arquitectura, tecnologías, requisitos y controles técnicos implementados en la versión **v1.0** del Sistema Unidad Territorial (SUT).

El documento describe únicamente capacidades implementadas, probadas o verificadas dentro del proyecto.

---

## 2. Alcance

El SUT es una aplicación web orientada a apoyar la gestión administrativa y comunitaria de una junta de vecinos.

La versión v1.0 permite gestionar:

- vecinos y membresía;
- proyectos vecinales;
- certificados de residencia;
- reservas de espacios;
- actividades y cupos;
- noticias y avisos;
- autenticación, roles y permisos;
- notificaciones por correo electrónico.

El sistema utiliza PostgreSQL y se ejecuta mediante Docker Compose en el entorno de desarrollo y demostración.

---

## 3. Tecnologías y arquitectura

| Componente | Tecnología | Uso |
|---|---|---|
| Lenguaje | Python 3.14 | Lógica de aplicación |
| Framework | Django 6.1.3 | Aplicación web, ORM, autenticación y pruebas |
| Base de datos | PostgreSQL 18 | Persistencia e integridad |
| Interfaz | Django Templates + Bootstrap 5.3.3 | Interfaz web responsiva |
| Documentos | ReportLab | Generación de certificados PDF |
| Contenedores | Docker + Docker Compose | Entorno reproducible |
| Versionamiento | Git + GitHub | Historial y trazabilidad |
| Gestión | Jira + Scrum | Planificación y seguimiento |

El proyecto utiliza una arquitectura web monolítica modular basada en aplicaciones Django.

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

El entorno Docker utiliza un contenedor web y PostgreSQL con volumen persistente.

El proceso web se ejecuta mediante un usuario sin privilegios root.

Respaldo gráfico:

```text
docs/diagramas/01-arquitectura-sut.svg
```

---

## 4. Requisitos funcionales

### RF-01 · Gestión de vecinos

El sistema permite:

- registrar usuarios;
- asociar un perfil de vecino;
- editar datos personales;
- gestionar vecinos desde perfiles autorizados;
- incorporar o retirar la condición de miembro de junta.

Los privilegios administrativos no pueden asignarse desde el registro público.

---

### RF-02 · Proyectos vecinales

Flujo:

```text
Miembro de junta
        ↓
Postulación
        ↓
Revisión
        ↓
Aprobación / Rechazo
```

Controles principales:

- sólo miembros de junta pueden postular;
- propietario y estado se asignan desde el servidor;
- cada usuario consulta únicamente los proyectos que le corresponden;
- Directiva y personal autorizado pueden resolver;
- se impide resolver dos veces;
- los estados válidos están restringidos en PostgreSQL;
- la resolución utiliza transacciones y `select_for_update()`.

---

### RF-03 · Resolución de proyectos por correo

La resolución puede notificarse al postulante mediante correo electrónico.

Se encuentra implementado:

- correo de aprobación y rechazo;
- destinatario asociado al postulante;
- correo HTML;
- tratamiento de usuarios sin email;
- tolerancia ante fallos SMTP.

Un fallo del servicio de correo no revierte una resolución ya registrada.

La integración SMTP externa fue validada mediante recorrido funcional.

---

### RF-04 · Certificados de residencia

Flujo:

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

Controles principales:

- la solicitud pertenece al vecino autenticado;
- se controla la existencia de solicitudes activas;
- sólo personal autorizado puede resolver;
- se impide la doble resolución y emisión;
- los estados están restringidos en PostgreSQL;
- la emisión utiliza transacción y `select_for_update()`;
- el certificado conserva un snapshot de los datos del vecino.

El sistema además permite:

- generar el certificado en PDF;
- visualizarlo y descargarlo desde la cuenta correspondiente;
- enviarlo como archivo adjunto por correo;
- conservar el estado emitido aunque falle posteriormente SMTP.

---

### RF-05 · Reservas

El sistema permite:

- reservar espacios activos;
- consultar reservas propias;
- visualizar un calendario mensual;
- administrar espacios;
- validar fechas y horarios;
- detectar solapamientos;
- excluir reservas canceladas de la disponibilidad.

La creación utiliza transacciones y bloqueo del espacio para volver a validar disponibilidad antes de guardar.

---

### RF-06 · Actividades

Para vecinos:

- consultar actividades;
- inscribirse;
- consultar inscripciones;
- impedir duplicados;
- controlar cupos.

La inscripción utiliza transacción y bloqueo de la actividad.

Para Directiva y personal autorizado:

- crear actividades;
- editar actividades;
- gestionar fechas y cupos;
- consultar inscritos;
- eliminar actividades sin inscripciones;
- impedir eliminar actividades con inscritos.

---

### RF-07 · Comunicaciones

El sistema permite:

- publicar noticias;
- publicar avisos;
- consultar comunicaciones públicamente;
- visualizar avisos destacados;
- crear, editar y eliminar publicaciones desde perfiles autorizados.

El contenido se presenta mediante Django Templates con escape automático.

---

### RF-08 · Autenticación y autorización

El sistema diferencia entre:

- vecino;
- miembro de junta;
- Directiva;
- personal autorizado;
- superusuario.

Los permisos funcionales se validan del lado del servidor mediante reglas centralizadas.

La autenticación determina quién es el usuario y la autorización qué operaciones puede ejecutar.

---

## 5. Requisitos no funcionales

| ID | Requisito | Respaldo |
|---|---|---|
| RNF-01 | Mantener configuración sensible fuera del repositorio | Variables de entorno, `.gitignore`, `.dockerignore` y `.env.example` |
| RNF-02 | Controlar acceso según permisos | Autorización centralizada y pruebas |
| RNF-03 | Mantener separación modular | 7 aplicaciones Django |
| RNF-04 | Proporcionar persistencia relacional | PostgreSQL 18 + Django ORM |
| RNF-05 | Mantener integridad de datos | Validaciones, transacciones y constraints |
| RNF-06 | Reducir condiciones de carrera | `transaction.atomic()` y `select_for_update()` |
| RNF-07 | Permitir reproducción del entorno | Dockerfile + Docker Compose |
| RNF-08 | Proporcionar interfaz adaptable | Django Templates + Bootstrap |
| RNF-09 | Mantener trazabilidad | Git, GitHub, Jira, pruebas y documentación |
| RNF-10 | Ejecutar el proceso sin privilegios root | Usuario no privilegiado en el contenedor |
| RNF-11 | Mantener credenciales fuera del código | Configuración mediante `.env` |
| RNF-12 | Mantener persistencia independiente del contenedor | Volumen PostgreSQL |

No se declaran métricas productivas de carga, rendimiento o disponibilidad porque no fueron medidas formalmente.

---

## 6. Seguridad e integridad

Los controles se aplican en distintas capas:

```text
Formulario
    ↓
Vista / autorización
    ↓
Reglas de negocio
    ↓
Transacción
    ↓
PostgreSQL
```

Entre los controles implementados se encuentran:

- protección CSRF;
- autorización del lado del servidor;
- aislamiento de información por usuario;
- constraints de integridad;
- prevención de operaciones duplicadas;
- transacciones atómicas;
- `select_for_update()` en operaciones sensibles;
- secretos fuera del código fuente;
- `.env` excluido del repositorio;
- escape automático de contenido;
- protección de descargas privadas;
- contenedor web sin privilegios root.

Las operaciones transaccionales más relevantes corresponden a:

- resolución de proyectos;
- emisión de certificados;
- creación de reservas;
- inscripción en actividades.

La configuración permite habilitar medidas adicionales para HTTPS, como cookies seguras, redirección SSL y HSTS.

Estas opciones representan preparación configurable y no un despliegue productivo demostrado.

---

## 7. Pruebas y verificación

La suite automatizada contiene:

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

Último resultado:

```text
Found 133 test(s).
Ran 133 tests
OK
```

Las pruebas cubren, entre otros aspectos:

- autenticación y autorización;
- aislamiento por usuario;
- restricciones por rol;
- estados y operaciones duplicadas;
- concurrencia;
- reservas solapadas;
- cupos de actividades;
- proyectos;
- certificados y PDF;
- fallos simulados de SMTP;
- CRUD administrativos.

También se realizaron recorridos End to End manuales sobre los flujos críticos de:

- certificados;
- proyectos;
- gestión de actividades.

El comportamiento general fue validado en escritorio y dispositivo móvil.

Último checkpoint técnico:

```text
Django check            OK
Pruebas                 133/133
Migraciones pendientes  ninguna
PostgreSQL              healthy
Aplicación Django       healthy
E2E crítico             verificado
```

El detalle de pruebas se mantiene en:

```text
docs/pruebas/
```

---

## 8. Ejecución

Crear `.env` a partir de `.env.example`.

Levantar el entorno:

```bash
docker compose up -d --build
```

Verificar servicios:

```bash
docker compose ps
```

Verificar Django:

```bash
docker compose exec -T web python manage.py check
```

Ejecutar pruebas:

```bash
docker compose exec -T web python manage.py test --verbosity 1
```

Verificar cambios pendientes en modelos:

```bash
docker compose exec -T web python manage.py makemigrations --check --dry-run
```

---

## 9. Límites de la versión v1.0

No forman parte de la implementación demostrada:

- integración directa con WhatsApp;
- pruebas End to End automatizadas mediante navegador;
- despliegue productivo en infraestructura externa;
- pruebas formales de carga o rendimiento.

La propuesta original contempla comunicaciones mediante aviso, correo y/o WhatsApp.

La versión v1.0 utiliza avisos dentro del sistema y correo electrónico.

La integración directa con WhatsApp queda fuera del alcance implementado.