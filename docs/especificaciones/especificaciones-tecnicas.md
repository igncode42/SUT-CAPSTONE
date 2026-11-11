# Especificaciones técnicas · Sistema Unidad Territorial

## 1. Objetivo

Documentar la arquitectura, tecnologías, requisitos y controles técnicos implementados en la versión **v1.0** del Sistema Unidad Territorial (SUT).

El documento describe únicamente capacidades implementadas, probadas o verificadas dentro del proyecto.

---

## 2. Alcance

El SUT es una aplicación web orientada a apoyar la gestión administrativa y comunitaria de una junta de vecinos.

La versión v1.0 contempla:

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

El sistema utiliza una arquitectura web monolítica modular basada en aplicaciones Django:

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

Docker Compose utiliza un contenedor para la aplicación web y otro para PostgreSQL con volumen persistente.

El proceso web se ejecuta mediante un usuario sin privilegios root.

Respaldo:

```text
docs/diagramas/01-arquitectura-sut.svg
```

### 3.1 Modelo de datos

El SUT utiliza un modelo relacional implementado mediante Django ORM sobre PostgreSQL.

Las principales relaciones son:

- un rol puede asociarse a varios usuarios;
- cada vecino se relaciona con una cuenta de usuario;
- un vecino puede registrar proyectos y solicitudes de certificado;
- una solicitud emitida puede generar un certificado;
- un vecino puede realizar varias reservas;
- vecinos y actividades se relacionan mediante inscripciones;
- usuarios autorizados pueden publicar noticias y avisos.

Las relaciones se implementan mediante claves foráneas y relaciones uno a uno según corresponda.

El modelo incorpora restricciones para proteger estados válidos, solicitudes activas, horarios e inscripciones duplicadas.

El modelo físico está implementado en PostgreSQL mediante los modelos Django y **15 migraciones**.

Respaldo:

```text
docs/diagramas/02-modelo-datos-sut.svg
```

### 3.2 Diagramas de respaldo

La documentación gráfica se encuentra en `docs/diagramas/`:

- `01-arquitectura-sut.svg`: arquitectura general;
- `02-modelo-datos-sut.svg`: modelo entidad-relación;
- `03-proceso-proyecto-vecinal.svg`: flujo de proyectos;
- `04-proceso-reserva-espacio.svg`: flujo de reservas;
- `05-proceso-actividad-cupos.svg`: flujo de actividades;
- `06-secuencia-certificado.svg`: secuencia UML de certificados;
- `07-proceso-proyecto-vecinal-bpmn.svg`: proceso BPMN de proyectos vecinales.

---

## 4. Requisitos funcionales

### RF-01 · Gestión de vecinos

El sistema permite:

- registro de usuarios y perfil de vecino;
- edición de datos personales;
- gestión interna de vecinos;
- incorporación y retiro de membresía de junta.

Los privilegios administrativos no pueden asignarse desde el registro público.

### RF-02 · Proyectos vecinales

Flujo principal:

```text
Miembro de junta
    ↓
Postulación
    ↓
Revisión
    ↓
Aprobación / Rechazo
```

Controles:

- sólo miembros pueden postular;
- propietario y estado se asignan desde el servidor;
- cada usuario accede únicamente a sus proyectos;
- usuarios autorizados pueden resolver;
- una resolución no puede ejecutarse dos veces;
- los estados están restringidos en la base de datos;
- la resolución utiliza transacciones y bloqueo del registro.

### RF-03 · Notificación de proyectos

La resolución puede notificarse al postulante mediante correo electrónico.

Se encuentra implementado:

- correo de aprobación y rechazo;
- destinatario asociado al postulante;
- contenido HTML;
- tratamiento de usuarios sin email;
- tolerancia ante fallos SMTP.

Un fallo del servicio de correo no revierte una resolución ya almacenada.

La integración SMTP externa fue verificada mediante recorrido funcional.

### RF-04 · Certificados de residencia

Flujo principal:

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

Controles:

- la solicitud pertenece al vecino autenticado;
- se controlan solicitudes activas;
- sólo personal autorizado puede resolver;
- se impide doble resolución y emisión;
- los estados están restringidos en PostgreSQL;
- la emisión utiliza transacción y bloqueo;
- el certificado conserva un snapshot de los datos utilizados.

El sistema permite además visualizar, descargar y enviar el PDF por correo desde el flujo autorizado.

Un fallo SMTP posterior no revierte un certificado ya emitido.

### RF-05 · Reservas

El sistema permite:

- reservar espacios activos;
- consultar reservas propias;
- visualizar un calendario mensual;
- administrar espacios mediante Django Admin;
- validar fechas y horarios;
- detectar solapamientos;
- excluir reservas canceladas de la disponibilidad.

La creación utiliza una transacción y bloqueo del espacio antes de volver a validar su disponibilidad.

### RF-06 · Actividades

Los vecinos pueden:

- consultar actividades;
- inscribirse;
- consultar sus inscripciones;
- participar según disponibilidad de cupos.

Directiva y personal autorizado pueden:

- crear y editar actividades;
- gestionar fechas y cupos;
- consultar inscritos;
- eliminar actividades sin inscripciones.

El sistema evita inscripciones duplicadas y protege actividades que ya poseen inscritos.

La inscripción utiliza transacción y bloqueo de la actividad.

### RF-07 · Comunicaciones

El sistema permite:

- publicar noticias y avisos;
- consultar comunicaciones públicamente;
- visualizar avisos destacados;
- crear, editar y eliminar publicaciones desde perfiles autorizados.

Las publicaciones se presentan mediante Django Templates con escape automático de contenido.

### RF-08 · Autenticación y autorización

El sistema diferencia entre:

- vecino;
- miembro de junta;
- Directiva;
- personal autorizado;
- superusuario.

La autenticación identifica al usuario y la autorización determina las operaciones que puede ejecutar.

Los permisos funcionales se validan en el servidor mediante reglas centralizadas.

---

## 5. Requisitos no funcionales

| ID | Requisito | Respaldo |
|---|---|---|
| RNF-01 | Mantener configuración sensible fuera del repositorio | Variables de entorno y `.env.example` |
| RNF-02 | Controlar acceso según permisos | Autorización centralizada y pruebas |
| RNF-03 | Mantener separación modular | 7 aplicaciones Django |
| RNF-04 | Proporcionar persistencia relacional | PostgreSQL + Django ORM |
| RNF-05 | Mantener integridad de datos | Validaciones, transacciones y constraints |
| RNF-06 | Reducir condiciones de carrera | `transaction.atomic()` y `select_for_update()` |
| RNF-07 | Permitir reproducción del entorno | Dockerfile + Docker Compose |
| RNF-08 | Proporcionar interfaz adaptable | Django Templates + Bootstrap |
| RNF-09 | Mantener trazabilidad | Git, GitHub, Jira, pruebas y documentación |
| RNF-10 | Ejecutar el proceso web sin privilegios root | Usuario no privilegiado |
| RNF-11 | Mantener credenciales fuera del código | Configuración mediante `.env` |
| RNF-12 | Mantener persistencia independiente del contenedor | Volumen PostgreSQL |

No se declaran métricas productivas de carga, rendimiento o disponibilidad porque no fueron medidas formalmente.

---

## 6. Seguridad e integridad

Los controles técnicos se aplican en distintas capas:

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
- aislamiento de información según usuario;
- constraints de integridad;
- prevención de operaciones duplicadas;
- transacciones atómicas;
- bloqueos mediante `select_for_update()` en operaciones sensibles;
- secretos fuera del código fuente;
- `.env` excluido del repositorio;
- escape automático de Django Templates;
- protección de descargas privadas;
- contenedor web sin privilegios root.

Las principales operaciones protegidas mediante transacciones y bloqueos corresponden a:

- resolución de proyectos;
- emisión de certificados;
- creación de reservas;
- inscripción en actividades.

Estos mecanismos reducen condiciones de carrera, aunque **no se realizó una prueba multihilo específica de concurrencia**.

La configuración permite habilitar medidas para HTTPS como cookies seguras, redirección SSL y HSTS.

Estas opciones corresponden a preparación configurable y no representan un despliegue productivo demostrado.

### Verificaciones técnicas

En el cierre de la versión se verificó:

- proceso web ejecutado como usuario `sut`;
- historial Git sin secretos detectados mediante Gitleaks;
- dependencias sin vulnerabilidades conocidas mediante pip-audit;
- `manage.py check --deploy` sin incidencias bajo perfil seguro simulado.

Respaldo:

```text
docs/evidencias/fase-2.2/28-seguridad-checks-ok.png
```

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

Último resultado verificado:

```text
Found 133 test(s).
Ran 133 tests
OK
```

La suite cubre principalmente:

- autenticación y autorización;
- aislamiento de información;
- permisos por rol;
- validaciones y reglas de negocio;
- estados y operaciones duplicadas;
- reservas solapadas;
- cupos de actividades;
- proyectos y certificados;
- generación de PDF;
- fallos simulados de SMTP;
- operaciones administrativas.

También se realizaron recorridos End to End manuales sobre:

- proyectos y correo;
- certificados, PDF y correo;
- reservas y calendario;
- actividades y cupos;
- comunicaciones y visualización responsive.

Respaldo:

```text
docs/evidencias/fase-2.2/27-pruebas-133-ok.png
docs/evidencias/fase-2.2/29-proyecto-resuelto-correo.png
docs/evidencias/fase-2.2/30-certificado-pdf-correo.png
docs/evidencias/fase-2.2/31-reserva-calendario.png
docs/evidencias/fase-2.2/32-actividad-cupos.png
docs/evidencias/fase-2.2/33-comunicaciones-responsive.png
```

El detalle de la estrategia y el Plan de Pruebas se encuentra en:

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

Verificar migraciones pendientes:

```bash
docker compose exec -T web python manage.py makemigrations --check --dry-run
```

Último checkpoint:

```text
Django check            OK
Pruebas                 133/133
Migraciones pendientes  ninguna
PostgreSQL              healthy
Aplicación Django       healthy
```

---

## 9. Límites de la versión v1.0

No forman parte del alcance demostrado:

- integración directa con WhatsApp;
- pruebas End to End automatizadas mediante navegador;
- despliegue productivo en infraestructura externa;
- pruebas formales de carga o rendimiento.

La propuesta original contempla comunicaciones mediante aviso, correo y/o WhatsApp.

La versión v1.0 utiliza avisos dentro del sistema y correo electrónico. La integración directa con WhatsApp queda fuera del alcance implementado.