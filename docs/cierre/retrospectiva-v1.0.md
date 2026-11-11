# Retrospectiva del proyecto — Sistema Unidad Territorial v1.0

## Objetivo

Revisar el desarrollo del SUT, identificando las principales dificultades, decisiones tomadas y aprendizajes obtenidos.

## Retrospectiva

| Aspecto | Situación | Acción realizada | Aprendizaje |
|---|---|---|---|
| Alcance | El sistema incluía varias funcionalidades relacionadas entre sí. | Se priorizaron las funcionalidades principales y se avanzó de forma incremental. | Definir y priorizar el alcance desde el inicio facilita mantener el trabajo controlado. |
| Integración | Los cambios en un módulo podían afectar otras partes del sistema. | Se realizaron pruebas progresivas antes de continuar con nuevos cambios. | Validar cada incremento permite detectar problemas antes de que se acumulen. |
| Tiempo | Desarrollo, pruebas y documentación debían avanzar dentro del mismo periodo académico. | Se reorganizaron tareas y se priorizó lo necesario para cada entrega. | Documentar durante el desarrollo reduce trabajo pendiente al cierre. |
| Seguridad e integridad | Algunas operaciones requerían evitar accesos indebidos, duplicados y problemas de concurrencia. | Se incorporaron permisos, validaciones, restricciones, transacciones y bloqueos. | La seguridad y la integridad deben considerarse desde el diseño. |
| Seguimiento | Era necesario mantener coherencia entre planificación, código, pruebas y documentación. | Se utilizaron Jira, Git/GitHub y documentación técnica para registrar el avance. | Mantener trazabilidad facilita comprobar el estado real del sistema y preparar su cierre. |

## Conclusión

La principal lección fue la importancia de avanzar de forma incremental y validar continuamente lo implementado.

En futuros proyectos priorizaría antes el alcance, mantendría la documentación actualizada durante el desarrollo y conservaría las pruebas como parte permanente del proceso.