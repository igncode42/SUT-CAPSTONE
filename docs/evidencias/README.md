# Evidencias — Sistema Unidad Territorial

Las evidencias del SUT se conservan por checkpoint para mantener la trazabilidad histórica del proyecto.

Una captura respalda únicamente el estado y resultado visible en el momento en que fue generada. No debe interpretarse automáticamente como evidencia del estado actual del sistema.

## Evidencias 01–16 — versión inicial

Corresponden principalmente a la base técnica, documental y metodológica de la primera versión del proyecto.

Incluyen evidencia de:

- interfaz inicial;
- administración Django;
- PostgreSQL;
- repositorio GitHub;
- configuración y protección de secretos;
- backlog y priorización;
- tablero Jira;
- primeras ejecuciones de pruebas;
- Docker.

Estas capturas se conservan como evidencia histórica y no representan por sí solas el estado actual del SUT.

## Evidencias 17–25 — Fase 2.1

- `17-pruebas-automatizadas-41-ok.png`: suite automatizada disponible en ese checkpoint.
- `18-docker-servicios-healthy.png`: servicios `sut-web` y `sut-postgres` saludables.
- `19-http-200-ok.png`: respuesta HTTP 200 del sistema.
- `20-proyecto-postulacion.png` a `22-proyecto-resuelto-aprobado.png`: recorrido manual de Proyectos.
- `23-certificado-solicitud-pendiente.png` a `25-certificado-emitido.png`: recorrido manual de Certificados.

Estas evidencias corresponden al estado alcanzado durante la Fase 2.1.

## Evidencias Fase 2.2

La evidencia final de la Entrega 2.2 se mantiene separada de los checkpoints anteriores.

Debe respaldar únicamente funcionalidades y resultados efectivamente implementados o demostrados en el estado final del proyecto, incluyendo según corresponda:

- ejecución del sistema;
- funcionalidades principales;
- pruebas automatizadas;
- arquitectura y persistencia;
- controles técnicos relevantes;
- recorridos funcionales utilizados en la demostración.

Las evidencias finales se incorporan después de verificar el estado técnico definitivo del SUT.

## Fuente de verdad

Para el estado actual del proyecto se consideran en conjunto:

`Código → Pruebas → Jira → Evidencias → Documentación`

Las capturas históricas permiten demostrar evolución, pero no reemplazan el código, las pruebas ni la documentación vigente.