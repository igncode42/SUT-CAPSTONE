# Avance Fase 2 — Sistema Unidad Territorial

**Fecha de referencia:** 10 de octubre de 2026
**Proyecto:** Sistema Unidad Territorial — SUT
**Estado:** Desarrollo en progreso

---

## 1. Propósito del documento

Registrar el estado actual del proyecto durante la Fase 2 de Capstone, identificando:

- avances realizados;
- funcionalidades implementadas;
- pruebas ejecutadas;
- dificultades encontradas;
- ajustes realizados durante el desarrollo;
- elementos pendientes para las siguientes iteraciones.

Este documento representa un checkpoint del proyecto y no corresponde al cierre final del SUT.

---

## 2. Evolución desde la versión v0.1

La versión v0.1 permitió establecer una primera base técnica compuesta principalmente por:

- proyecto Django;
- aplicaciones organizadas por dominio;
- modelos de datos;
- migraciones;
- PostgreSQL;
- Django Admin;
- diagramas iniciales;
- documentación base;
- dos pruebas automatizadas iniciales.

Durante la Fase 2 esta base fue utilizada para comenzar a implementar los flujos funcionales y reglas de negocio prioritarias.

La evolución principal puede resumirse de la siguiente manera:

```text
v0.1
↓
Autenticación
↓
Autorización / RBAC
↓
Proyectos vecinales
↓
Resolución de proyectos
↓
Notificación por correo
↓
Certificados
↓
Dockerización completa del entorno
↓
41 pruebas automatizadas
```

---

## 3. Estado general actual

| Área | Estado |
|---|---|
| Django | Implementado |
| PostgreSQL | Implementado |
| Docker Compose | Implementado y verificado |
| Autenticación | Implementada y probada |
| Autorización / RBAC | Implementada y probada |
| Proyectos vecinales | Flujo principal implementado y probado |
| Certificados | Flujo principal implementado y probado |
| Correo de resolución de proyectos | Implementado y probado en entorno de desarrollo |
| Pruebas automatizadas | 41 aprobadas |
| Modelo de datos | Implementado |
| Diagramas base | Disponibles; arquitectura actualizada con Docker Compose |
| Reservas | Implementación parcial |
| Actividades | Implementación parcial |
| Comunicaciones | Implementación parcial |
| Plan formal de pruebas | Completado para el checkpoint actual |
| Evidencias visuales | Actualizadas para los flujos principales y entorno técnico |
| Jira / Scrum | Requiere sincronización final antes del envío |

---

## 4. Avances de producto

### 4.1 Autenticación y autorización

Se implementó:

- inicio de sesión;
- cierre de sesión;
- panel privado;
- protección de vistas;
- permisos centralizados;
- distinción entre usuario autenticado y usuario autorizado;
- acceso específico para miembros de junta;
- permisos para personal autorizado / Directiva.

Las reglas fueron verificadas mediante pruebas positivas y negativas.

---

### 4.2 Proyectos vecinales

Se implementó el flujo:

```text
Miembro de junta
↓
Postular proyecto
↓
PENDIENTE
↓
Revisión
↓
APROBADO / RECHAZADO
↓
Notificación
```

El sistema permite:

- postular proyectos únicamente a usuarios autorizados;
- asociar automáticamente el proyecto al vecino autenticado;
- impedir manipulación manual del propietario y estado;
- visualizar únicamente proyectos propios;
- revisar proyectos pendientes;
- aprobar o rechazar;
- impedir una segunda resolución de un proyecto ya procesado;
- generar una notificación por correo al resolver el proyecto.

La integración actual de correo utiliza el backend de desarrollo de Django.

La configuración de SMTP externo permanece pendiente.

---

### 4.3 Certificados

Se implementó el flujo:

```text
Vecino
↓
Solicitar certificado
↓
PENDIENTE
↓
Revisión
↓
APROBADA / RECHAZADA
↓
EMITIDA
```

Actualmente se permite:

- crear solicitudes asociadas al vecino autenticado;
- consultar únicamente solicitudes propias;
- revisar solicitudes pendientes;
- aprobar o rechazar;
- emitir una solicitud previamente aprobada;
- crear la entidad `Certificado`;
- impedir emisión de solicitudes rechazadas;
- impedir emisión duplicada.

Actualmente la emisión corresponde a una entidad registrada en el sistema.

La generación de un archivo o PDF descargable permanece pendiente.

---

## 5. Infraestructura y Docker

Inicialmente PostgreSQL se ejecutaba mediante Docker mientras Django se ejecutaba directamente desde Windows.

Durante esta iteración se amplió la dockerización para incluir ambos componentes.

La arquitectura de ejecución actual es:

```text
Docker Compose
├── sut-web
│   └── Django
│
└── sut-postgres
    └── PostgreSQL
```

Se incorporaron:

- `Dockerfile`;
- `.dockerignore`;
- servicio web en `compose.yml`;
- healthcheck de PostgreSQL;
- healthcheck de Django;
- dependencia del servicio web respecto al estado saludable de la base de datos;
- ejecución automática de migraciones al iniciar el servicio.

Estado verificado:

```text
sut-web        healthy
sut-postgres   healthy
HTTP           200
Django check   OK
```

La configuración actual está orientada a desarrollo y demostración del proyecto.

No se presenta como una configuración de producción definitiva.

---

## 6. Pruebas y calidad

La suite automatizada evolucionó desde dos pruebas iniciales hasta:

**41 pruebas automatizadas.**

Distribución actual:

```text
Autenticación y autorización   11
Proyectos                      17
Certificados                   13
─────────────────────────────────
Total                          41
```

Resultado:

```text
41 aprobadas
0 fallidas
```

Las pruebas consideran:

- casos exitosos;
- accesos anónimos;
- usuarios sin permisos;
- aislamiento de información;
- reglas de negocio;
- operaciones inválidas;
- transiciones de estado;
- operaciones duplicadas;
- notificaciones.

El checkpoint actual de la suite fue ejecutado correctamente dentro del contenedor Docker de Django.

---

## 7. Factores que facilitaron el avance

Los principales factores que han facilitado el desarrollo son:

- arquitectura modular mediante aplicaciones Django;
- uso de PostgreSQL desde las primeras etapas;
- control de versiones mediante Git y GitHub;
- desarrollo incremental;
- incorporación temprana de pruebas automatizadas;
- centralización de permisos para reutilizar reglas de autorización;
- Docker Compose para reproducir el entorno;
- división del trabajo en incrementos pequeños y verificables.

La reutilización de patrones entre Proyectos y Certificados permitió acelerar el desarrollo de nuevas funcionalidades manteniendo una estructura consistente.

---

## 8. Dificultades encontradas

Durante el desarrollo se encontraron principalmente las siguientes dificultades:

### Configuración del entorno

La ejecución local presentó diferencias entre el entorno Windows y los contenedores Docker, especialmente en la conexión a PostgreSQL.

Se resolvió diferenciando:

```text
Windows → 127.0.0.1:5433
Docker  → db:5432
```

---

### Autenticación y rutas

Durante la implementación inicial se detectó una diferencia entre la ruta de login esperada por Django y la ruta configurada en el proyecto.

La configuración fue centralizada mediante `LOGIN_URL`.

---

### Pruebas frágiles

Una prueba asumía que una solicitud tendría siempre el identificador `1`.

Al ejecutarse junto con el resto de la suite, el identificador podía ser diferente.

La prueba fue corregida utilizando el identificador real generado por la base de datos.

Esto permitió evitar dependencias innecesarias entre casos de prueba.

---

### Documentación desactualizada

El desarrollo funcional avanzó más rápido que algunos documentos y evidencias.

Como resultado, archivos anteriores continuaban mostrando:

- dos pruebas automatizadas;
- permisos pendientes;
- Proyectos sin flujo funcional;
- Certificados sin emisión;
- Dockerización parcial.

Se inició una etapa de sincronización documental para alinear documentación, código y evidencias.

---

### Desarrollo individual

El proyecto se encuentra siendo desarrollado de forma individual.

Esto requiere priorizar los elementos de mayor impacto y evitar implementar simultáneamente todos los módulos del sistema.

---

## 9. Ajustes realizados durante la Fase 2

Durante el desarrollo se realizaron los siguientes ajustes:

### Metodología

La gestión actual se organiza mediante Scrum apoyado por Jira.

---

### Priorización

Se priorizaron los siguientes elementos:

1. infraestructura;
2. autenticación;
3. autorización;
4. Proyectos;
5. Certificados;
6. pruebas;
7. Dockerización;
8. documentación y evidencia.

Los módulos de Reservas, Actividades y Comunicaciones se mantuvieron como desarrollo posterior para evitar distribuir el esfuerzo entre demasiados frentes simultáneamente.

---

### Calidad

Se adoptó como criterio de trabajo:

```text
Implementar
↓
Probar
↓
Corregir
↓
Commit
↓
Documentar
↓
Evidenciar
```

Esto permitió detectar errores antes de integrarlos al historial principal del proyecto.

---

### Evidencia

Se comenzó a distinguir explícitamente entre:

```text
Diseñado
≠
Implementado
≠
Probado
≠
Evidenciado
```

Esta distinción permite representar el estado real del proyecto sin presentar como terminadas funcionalidades que todavía se encuentran en desarrollo.

Evidencias principales del checkpoint:

- `17-pruebas-automatizadas-41-ok.png`: ejecución de la suite automatizada;
- `18-docker-servicios-healthy.png`: servicios Docker saludables;
- `19-http-200-ok.png`: respuesta HTTP 200;
- `20-proyecto-postulacion.png` a `22-proyecto-resuelto-aprobado.png`: flujo de Proyectos;
- `23-certificado-solicitud-pendiente.png` a `25-certificado-emitido.png`: flujo de Certificados.

---

## 10. Desarrollo pendiente

### Prioridad inmediata

- sincronizar Jira/Scrum con los últimos incrementos;
- realizar commit y push del checkpoint;
- preparar la carpeta compartida solicitada por el docente;
- grabar el video breve de demostración del producto.

### Desarrollo funcional posterior

- registro/autogestión de vecinos;
- reservas y calendario;
- validación de disponibilidad;
- actividades e inscripciones;
- control de cupos;
- noticias y avisos para usuarios finales;
- generación de certificado descargable;
- integración SMTP externa;
- integración WhatsApp;
- pruebas End to End mediante navegador.

La prioridad de estos elementos podrá ajustarse según retroalimentación docente y planificación de los siguientes Sprints.

---

## 11. Estado verificable del checkpoint

```text
Django                         OK
PostgreSQL                     OK
Docker Compose                 OK
sut-web                        healthy
sut-postgres                   healthy
HTTP                           200
Autenticación                  implementada
RBAC                           implementado
Proyectos                      implementados
Certificados                   implementados
Pruebas automatizadas          41/41
Git / GitHub                   operativo
```

---

## 12. Próximo checkpoint

El checkpoint técnico queda consolidado con código, pruebas, documentación y evidencias alineadas.

Antes del envío de avance corresponde cerrar únicamente:

```text
Jira
↓
Commit / push
↓
Carpeta compartida
↓
Video de demostración
```

Los nuevos incrementos funcionales se retomarán después de recibir retroalimentación docente.