# Pruebas — Sistema Unidad Territorial

## Objetivo

Verificar comportamientos básicos de acceso y funcionamiento del sistema durante la etapa inicial de desarrollo.

## Pruebas ejecutadas

| ID | Prueba | Resultado |
|---|---|---|
| TEST-01 | La página principal puede accederse correctamente | Aprobada |
| TEST-02 | El panel administrativo requiere autenticación | Aprobada |

## Evidencia

Se ejecutaron las pruebas mediante el framework de testing integrado en Django.

Comando utilizado:

`python manage.py test`

## Resultado

Las pruebas definidas fueron ejecutadas correctamente.

## Pruebas futuras

- Validar que sólo miembros puedan postular proyectos.
- Validar que sólo personal autorizado pueda aprobar o rechazar proyectos.
- Evitar inscripciones cuando una actividad no disponga de cupos.
- Evitar reservas incompatibles para un mismo espacio.
- Validar permisos según rol.