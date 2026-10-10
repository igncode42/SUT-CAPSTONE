# Especificaciones técnicas — Sistema Unidad Territorial

## 1. Objetivo

Documentar el estado técnico actual del SUT, diferenciando lo implementado, lo verificado y lo pendiente durante la Fase 2 de Capstone.

---

## 2. Alcance actual

El SUT es una aplicación web orientada a apoyar procesos administrativos y comunitarios de una junta de vecinos.

### Implementado y verificado

- autenticación y cierre de sesión;
- autorización según perfil, rol y permisos del servidor;
- postulación, revisión y resolución de proyectos vecinales;
- solicitud, revisión y emisión lógica de certificados de residencia;
- persistencia en PostgreSQL;
- ejecución mediante Docker Compose;
- pruebas automatizadas para autenticación, autorización, proyectos y certificados.

### Implementado parcialmente

- vecinos: modelo, perfil y administración;
- reservas: modelos y administración;
- actividades: modelos y administración;
- comunicaciones: modelos y administración.

### Pendiente

- calendario y validación funcional de reservas;
- inscripción y control funcional de cupos;
- publicación de noticias y avisos para usuarios finales;
- certificado descargable;
- SMTP externo;
- integración WhatsApp;
- pruebas End to End automatizadas mediante navegador.

---

## 3. Tecnologías utilizadas

| Componente | Tecnología | Uso actual |
|---|---|---|
| Lenguaje | Python 3.14 | Lógica de aplicación |
| Framework | Django 6.1 | Aplicación web, autenticación, ORM y pruebas |
| Base de datos | PostgreSQL 18 | Persistencia principal |
| Interfaz | Django Templates + Bootstrap | Interfaz web responsiva |
| Contenedores | Docker + Docker Compose | Entorno reproducible de demostración |
| Control de versiones | Git + GitHub | Historial y respaldo técnico |
| Gestión | Jira + Scrum | Seguimiento del trabajo |

---

## 4. Arquitectura

El proyecto utiliza un monolito modular Django organizado por dominios. En el entorno dockerizado, el navegador accede a `sut-web` por el puerto 8000 y Django se comunica con `sut-postgres` mediante el servicio `db` de Docker Compose.

```text
Usuario
  ↓
Navegador
  ↓ http://127.0.0.1:8000
Docker Compose
  ├─ sut-web
  │   └─ Django → aplicaciones → Django ORM
  └─ sut-postgres
      └─ PostgreSQL 18
```

El backend de correo actual es de desarrollo. La conexión SMTP externa permanece pendiente.

Respaldo gráfico: `docs/diagramas/01-arquitectura-sut.*`.

---

## 5. Requisitos funcionales implementados

### Proyectos vecinales

`Miembro de junta → Postular → Pendiente → Directiva → Aprobar/Rechazar → Notificación`

Controles principales:

- sólo un miembro de junta puede postular;
- el propietario se determina en el servidor;
- el estado inicial se asigna en el servidor;
- cada usuario consulta únicamente sus propios proyectos;
- sólo personal autorizado resuelve;
- una postulación ya resuelta no puede resolverse nuevamente.

### Certificados

`Vecino → Solicitar → Pendiente → Directiva → Aprobar/Rechazar → Emitir`

Controles principales:

- la solicitud se asocia al vecino autenticado;
- cada vecino consulta únicamente sus solicitudes;
- sólo personal autorizado gestiona solicitudes;
- sólo una solicitud aprobada puede emitirse;
- se evita la emisión duplicada.

---

## 6. Requisitos no funcionales

| ID | Requisito | Estado | Respaldo |
|---|---|---|---|
| RNF-01 | Proteger configuración sensible fuera del repositorio | **Implementado** | variables de entorno, `.gitignore`, `.dockerignore`, `.env.example` |
| RNF-02 | Controlar acceso a operaciones según autenticación y autorización | **Implementado y probado** | middleware Django, permisos centralizados y pruebas negativas |
| RNF-03 | Mantener separación modular por dominio | **Implementado** | aplicaciones Django independientes por módulo |
| RNF-04 | Permitir reproducción del entorno de demostración | **Implementado y verificado** | `Dockerfile`, `compose.yml`, healthchecks |
| RNF-05 | Mantener integridad de estados y evitar operaciones duplicadas | **Implementado y probado** en Proyectos y Certificados | validaciones de servidor y pruebas automatizadas |
| RNF-06 | Mantener trazabilidad técnica del desarrollo | **Implementado** | Git/GitHub, documentación, evidencias y Jira |
| RNF-07 | Proveer una interfaz web adaptable mediante Bootstrap | **Implementado como base** | templates y Bootstrap; validación formal multidispositivo pendiente |
| RNF-08 | Mantener disponibilidad verificable del entorno de demostración | **Verificado en checkpoint** | healthchecks de `sut-web` y `sut-postgres`, HTTP 200 |

No se declaran métricas de rendimiento, carga o disponibilidad productiva porque no han sido medidas formalmente.

---

## 7. Configuración y ejecución

Crear un archivo `.env` local tomando `.env.example` como referencia. Los secretos reales no deben versionarse.

Levantar el entorno:

```bash
docker compose up -d --build
```

Verificar servicios:

```bash
docker compose ps
```

Ejecutar pruebas en Docker:

```bash
docker compose exec -T web python manage.py test --verbosity 1
```

Checkpoint verificado del avance:

```text
sut-web        healthy
sut-postgres   healthy
HTTP           200
Pruebas        41/41 OK
```

---

## 8. Evidencia y límites del avance

La evidencia técnica se mantiene en `docs/evidencias/` y el detalle de pruebas en `docs/pruebas/`.

Este documento describe el avance actual de Fase 2. No presenta Reservas, Actividades, Comunicaciones, SMTP externo ni certificado PDF como funcionalidades terminadas.
