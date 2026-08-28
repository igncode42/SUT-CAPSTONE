# Matriz de trazabilidad — SUT

| Necesidad / regla | Requisito | Implementación / diseño | Evidencia |
|---|---|---|---|
| Gestionar vecinos | RF-01 | Modelo Vecino | PostgreSQL + Admin |
| Solicitar certificados | RF-03 / RF-04 | SolicitudCertificado / Certificado | ERD + Admin + BD |
| Sólo miembros postulan proyectos | RN-01 / RF-05 | ProyectoVecinal + roles | Proceso proyecto + modelo |
| Directorio aprueba o rechaza | RN-02 / RF-06 | Estado ProyectoVecinal | Diagrama de proceso |
| Reservas mediante calendario | RN-04 / RF-09 | Espacio / Reserva | ERD + proceso reserva |
| Inscripción depende de cupos | RN-05 / RF-11 | Actividad / InscripcionActividad | ERD + proceso actividad |
| Publicar noticias y avisos | RF-13 | Noticia / Aviso | Admin + BD |
| Proteger acceso administrativo | RS-01 | Django Authentication | Test + panel admin |
| Proteger secretos | RS-05 | .env + .gitignore | Git |