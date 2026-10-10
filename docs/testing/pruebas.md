# Pruebas — Sistema Unidad Territorial

## 1. Objetivo

Verificar que las funcionalidades actualmente implementadas del Sistema Unidad Territorial (SUT) cumplan sus reglas de negocio, restricciones de acceso y comportamiento esperado.

Las pruebas buscan comprobar no sólo los casos exitosos, sino también situaciones inválidas o no autorizadas.

---

## 2. Estrategia de pruebas

El proyecto utiliza principalmente el framework de testing integrado de Django.

La estrategia actual prioriza pruebas funcionales y de integración sobre los módulos que ya poseen flujos de usuario implementados.

Se consideran principalmente:

- autenticación;
- autorización;
- permisos por rol;
- reglas de negocio;
- aislamiento de información entre usuarios;
- transiciones de estado;
- operaciones inválidas;
- duplicación de acciones;
- integración entre vistas, modelos y PostgreSQL;
- generación de notificaciones por correo.

Las pruebas End to End (E2E) mediante navegador completo no forman parte todavía de la suite automatizada actual.

Estas se incorporarán posteriormente sobre los flujos principales cuando corresponda.

---

## 3. Herramientas utilizadas

Actualmente se utilizan:

- Django TestCase;
- Django Test Client;
- PostgreSQL como motor de base de datos del proyecto;
- backend de correo en memoria para pruebas de notificaciones;
- Docker Compose para comprobar el funcionamiento del sistema en un entorno reproducible;
- Git y GitHub para mantener trazabilidad de los cambios.

---

## 3.1 Niveles de prueba y estado

| Nivel | Estado actual |
|---|---|
| Unitarias aisladas | No se mantienen como suite separada; las reglas se verifican principalmente mediante `TestCase` |
| Integración | Implementadas sobre vistas, modelos, base de datos y correo de testing |
| Funcionales | Implementadas y registradas en el Plan de Pruebas |
| Aceptación / UAT | Pendiente de ejecución formal |
| End to End | Casos definidos; ejecución automatizada mediante navegador pendiente |

Esta clasificación documenta el estado real del proyecto y no presenta como ejecutados niveles que todavía están pendientes.

---

## 4. Cobertura automatizada actual

La suite automatizada contiene actualmente:

**41 pruebas.**

Estas se distribuyen en los siguientes dominios.

### 4.1 Autenticación y autorización — 11 pruebas

Las pruebas de autenticación y permisos verifican principalmente:

- acceso público a la página principal;
- protección del panel administrativo;
- visualización de la página de login;
- protección del panel privado para usuarios no autenticados;
- acceso correcto de usuarios autenticados;
- redirección después de iniciar sesión;
- cierre de sesión;
- protección de zonas restringidas;
- acceso permitido para miembros de junta;
- rechazo de usuarios sin autorización;
- verificación de roles mediante permisos centralizados.

El objetivo es comprobar que autenticación y autorización se encuentren separadas correctamente.

Un usuario puede estar autenticado y, aun así, no tener permiso para ejecutar determinadas acciones.

---

### 4.2 Proyectos vecinales — 17 pruebas

Las pruebas del módulo de proyectos verifican el flujo:

`Miembro de junta → Postular → Pendiente → Revisar → Aprobar/Rechazar → Notificar`

Se comprueba:

- bloqueo de usuarios anónimos;
- bloqueo de usuarios sin permisos;
- postulación por miembros de junta;
- asociación automática del proyecto con el vecino autenticado;
- estado inicial `PENDIENTE`;
- protección frente a modificación manual del propietario o estado;
- visualización exclusiva de proyectos propios;
- acceso de Directiva a proyectos pendientes;
- aprobación de proyectos;
- rechazo de proyectos;
- prohibición de resolver proyectos por parte de vecinos sin autorización;
- protección contra doble resolución;
- generación de correo al aprobar;
- generación de correo al rechazar;
- destinatario correcto de la notificación;
- funcionamiento cuando el usuario no posee correo registrado;
- prevención de una segunda notificación cuando el proyecto ya fue resuelto.

---

### 4.3 Certificados — 13 pruebas

Las pruebas del módulo de certificados verifican el flujo:

`Vecino → Solicitar → Pendiente → Revisar → Aprobar/Rechazar → Emitir`

Se comprueba:

- bloqueo de usuarios anónimos;
- bloqueo de usuarios sin perfil de vecino;
- creación válida de una solicitud;
- estado inicial `PENDIENTE`;
- creación de solicitudes únicamente mediante petición POST;
- visualización exclusiva de solicitudes propias;
- acceso de Directiva a solicitudes pendientes;
- aprobación de solicitudes;
- rechazo de solicitudes;
- prohibición de emitir solicitudes rechazadas;
- emisión de solicitudes aprobadas;
- cambio de estado a `EMITIDA`;
- protección contra emisión duplicada.

---

## 5. Casos positivos y negativos

La estrategia de pruebas considera tanto comportamiento esperado como comportamiento prohibido.

Ejemplos de casos positivos:

- un miembro de junta puede postular un proyecto;
- una Directiva puede aprobar una postulación;
- un vecino puede solicitar un certificado;
- una solicitud aprobada puede ser emitida.

Ejemplos de casos negativos:

- un usuario anónimo no puede ingresar a zonas privadas;
- un vecino sin autorización no puede resolver proyectos;
- un usuario no puede visualizar información perteneciente a otro vecino;
- un proyecto resuelto no puede resolverse nuevamente;
- una solicitud rechazada no puede emitir un certificado;
- un certificado no puede ser emitido dos veces.

Los casos negativos permiten verificar que las reglas de negocio también se cumplen cuando un usuario intenta realizar una acción inválida.

---

## 6. Ejecución local disponible

Con el entorno virtual del proyecto activo:

```bash
python manage.py test --verbosity 1
```

Este comando permite ejecutar la misma suite desde el entorno virtual local. El checkpoint de esta entrega se verificó en Docker.

---

## 7. Ejecución mediante Docker

La suite también fue ejecutada dentro del contenedor Django del proyecto.

Comando:

```bash
docker compose exec -T web python manage.py test --verbosity 1
```

Resultado verificado:

```text
Found 41 test(s).
.........................................
OK
```

Este es el entorno utilizado para verificar el checkpoint actual de la entrega.

---

## 8. Estado actual

| Área | Estado |
|---|---|
| Autenticación | Probada |
| Autorización / RBAC | Probada |
| Proyectos vecinales | Probados |
| Notificación de proyectos | Probada con backend de testing |
| Certificados | Probados |
| PostgreSQL | Integrado |
| Docker Compose | Verificado |
| Reservas | Flujo funcional pendiente |
| Actividades | Flujo funcional pendiente |
| Comunicaciones | Flujo funcional pendiente |
| E2E con navegador | Pendiente |

Total actual:

**41 pruebas aprobadas / 0 fallidas.**

---

## 9. Diferencia entre pruebas automatizadas y Plan de Pruebas

Este documento resume la estrategia de testing implementada en el código del proyecto.

El Plan de Pruebas entregado por el docente corresponde a un documento formal diferente.

Las pruebas automatizadas pueden respaldar varios casos definidos en dicho plan.

Por esta razón:

`Pruebas automatizadas → evidencia técnica`

`Plan de Pruebas → planificación y registro formal`

Ambos elementos deben mantenerse relacionados.

---

## 10. Próximos pasos de testing

A medida que se implementen nuevos flujos se deberán incorporar pruebas para:

- disponibilidad de espacios;
- colisiones de reservas;
- actividades;
- control de cupos;
- inscripciones;
- noticias y avisos para usuarios finales;
- generación o descarga documental del certificado;
- integración SMTP externa;
- pruebas End to End sobre los principales recorridos del usuario.

La cantidad de pruebas deberá crecer en función de nuevas reglas y riesgos reales del sistema, no únicamente para aumentar el número total.