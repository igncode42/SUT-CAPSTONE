# Pruebas — Sistema Unidad Territorial

## 1. Objetivo

Verificar que las funcionalidades implementadas del Sistema Unidad Territorial (SUT) cumplan sus reglas de negocio, restricciones de acceso e integridad esperada.

La estrategia considera tanto operaciones válidas como intentos inválidos, accesos no autorizados y situaciones de borde.

## 2. Estrategia

El proyecto utiliza principalmente las herramientas de testing incluidas en Django:

- `TestCase`;
- Django Test Client;
- PostgreSQL como base de datos del sistema;
- backend de correo en memoria para pruebas automatizadas;
- Docker Compose para ejecutar la suite en un entorno reproducible.

Las pruebas cubren principalmente:

- autenticación y autorización;
- permisos por rol;
- aislamiento de datos;
- validaciones;
- reglas de negocio;
- transiciones de estado;
- operaciones duplicadas;
- restricciones de base de datos;
- integración entre vistas, modelos y PostgreSQL;
- comportamiento ante fallos controlados.

## 3. Niveles de prueba

| Nivel | Estado |
|---|---|
| Unitarias aisladas | No existe una suite separada; las reglas se validan principalmente mediante `TestCase` |
| Integración | Implementada sobre vistas, modelos, base de datos y correo |
| Funcionales | Implementadas |
| End to End manual | Ejecutados los flujos críticos de Proyectos y Certificados |
| End to End automatizado con navegador | No implementado |
| Carga / rendimiento | No ejecutado formalmente |

No se presentan como ejecutados niveles de prueba que no cuentan con evidencia verificable.

## 4. Suite automatizada

La suite actual contiene:

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

Último resultado verificado:

```text
Found 97 test(s).
Ran 97 tests
OK
```

La ejecución completa se realizó dentro del contenedor Django.

## 5. Cobertura principal

### Usuarios y permisos

Se verifican:

- acceso público y privado;
- login y logout;
- protección de vistas;
- permisos por rol;
- diferencia entre autenticación y autorización;
- rechazo de usuarios `staff` sin rol funcional;
- acceso de Directiva, personal autorizado y superusuario.

### Vecinos

Se verifican:

- registro;
- creación de usuario y perfil;
- validaciones;
- gestión de vecinos;
- control de membresía;
- prevención de autoasignación de privilegios;
- restricciones de acceso.

### Proyectos

Flujo:

`Miembro → Postulación → Pendiente → Revisión → Aprobación/Rechazo → Notificación`

Se verifican:

- permisos de postulación;
- asociación automática con el vecino;
- estado inicial;
- aislamiento de proyectos;
- aprobación y rechazo;
- protección contra doble resolución;
- estados válidos en PostgreSQL;
- envío de correo;
- ausencia de duplicación;
- comportamiento ante fallo SMTP.

El fallo SMTP se simula expresamente para comprobar que una caída del servicio externo no revierta una resolución ya guardada.

### Certificados

Flujo:

`Vecino → Solicitud → Revisión → Aprobación/Rechazo → Emisión`

Se verifican:

- creación válida;
- aislamiento de solicitudes;
- autorización;
- una única solicitud activa;
- aprobación y rechazo;
- prevención de doble resolución;
- emisión;
- prevención de doble emisión;
- estados válidos en PostgreSQL;
- conservación histórica de los datos utilizados al emitir el certificado.

### Reservas

Se verifican:

- creación válida;
- rechazo de fechas pasadas;
- hora de inicio anterior a la hora de término;
- restricción equivalente en PostgreSQL;
- estados válidos;
- detección de solapamientos;
- aceptación de horarios contiguos;
- bloqueo de espacios inactivos;
- aislamiento de reservas;
- calendario mensual;
- exclusión de reservas canceladas;
- manejo de parámetros de calendario inválidos.

La creación utiliza transacción, bloqueo del espacio y revalidación de su estado y de posibles solapamientos antes de guardar.

No se ha ejecutado una prueba multihilo específica de concurrencia.

### Actividades

Se verifican:

- inscripción válida;
- rechazo de duplicados;
- restricción única en base de datos;
- control de cupos;
- rechazo de actividades pasadas;
- validación de cupo mínimo.

La inscripción utiliza transacción y bloqueo de la actividad durante las comprobaciones de vigencia, duplicación y capacidad.

### Comunicaciones

Se verifican:

- publicación de noticias;
- publicación de avisos;
- permisos de publicación;
- acceso público;
- asociación del autor desde servidor;
- escape de contenido potencialmente peligroso.

## 6. Casos positivos y negativos

La suite combina escenarios permitidos y prohibidos.

Ejemplos positivos:

- un miembro puede postular un proyecto;
- una Directiva puede resolverlo;
- un vecino puede solicitar un certificado;
- una reserva válida puede registrarse;
- un vecino puede inscribirse mientras exista cupo.

Ejemplos negativos:

- un usuario anónimo no accede a zonas privadas;
- un usuario sin rol no ejecuta acciones administrativas;
- un proyecto resuelto no vuelve a resolverse;
- una solicitud rechazada no puede emitirse;
- una reserva solapada se rechaza;
- una inscripción duplicada se rechaza;
- un usuario no puede asignarse privilegios mediante formularios públicos.

Los casos negativos validan las reglas del sistema también frente a usos incorrectos o manipulaciones.

## 7. End to End manual

Se ejecutaron recorridos completos de los dos flujos críticos definidos en el Plan de Pruebas v0.1.

### Proyecto

Recorrido realizado:

`Registro → membresía → postulación → revisión → aprobación → notificación`

Se verificó el envío real de la resolución mediante un servidor SMTP externo.

### Certificado

Recorrido realizado:

`Solicitud → aprobación → emisión → visualización`

Se comprobó además que una solicitud emitida no pudiera volver a emitirse desde el flujo normal.

Estos recorridos fueron ejecutados manualmente y no mediante automatización de navegador.

## 8. Ejecución

Suite completa en Docker:

```bash
docker compose exec -T web python manage.py test --verbosity 1
```

Comprobación de configuración:

```bash
docker compose exec -T web python manage.py check
```

Verificación de cambios pendientes en modelos:

```bash
docker compose exec -T web python manage.py makemigrations --check --dry-run
```

Último checkpoint:

```text
Django check          OK
Pruebas               97/97
Migraciones nuevas    No changes detected
```

## 9. Plan de Pruebas

El código automatizado y el Plan de Pruebas cumplen funciones diferentes:

```text
Suite automatizada
→ evidencia técnica repetible

Plan de Pruebas
→ planificación y registro formal
```

`Plan_de_Pruebas_SUT_v0.1.xlsx` se conserva como evidencia histórica.

Para la Entrega 2.2 se preparará `Plan_de_Pruebas_SUT_v0.2.xlsx`, reflejando el estado final del sistema y los recorridos ejecutados.

## 10. Límites

Actualmente no se dispone de:

- pruebas End to End automatizadas mediante navegador;
- prueba multihilo específica para concurrencia;
- pruebas formales de carga;
- pruebas formales de rendimiento;
- pruebas de disponibilidad productiva.

Estas capacidades no se presentan como ejecutadas ni demostradas.