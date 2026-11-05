from django.db import models
from django.db.models import Q

from vecinos.models import Vecino


class SolicitudCertificado(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        APROBADA = "APROBADA", "Aprobada"
        RECHAZADA = "RECHAZADA", "Rechazada"
        EMITIDA = "EMITIDA", "Emitida"

    vecino = models.ForeignKey(
        Vecino,
        on_delete=models.CASCADE,
        related_name="solicitudes_certificado",
    )

    fecha_solicitud = models.DateTimeField(
        auto_now_add=True
    )

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["vecino"],
                condition=Q(
                    estado__in=[
                        "PENDIENTE",
                        "APROBADA",
                    ]
                ),
                name="solicitud_certificado_activa_unica_por_vecino",
            ),
            models.CheckConstraint(
                condition=Q(
                    estado__in=[
                        "PENDIENTE",
                        "APROBADA",
                        "RECHAZADA",
                        "EMITIDA",
                    ]
                ),
                name="solicitud_certificado_estado_valido",
            ),
        ]

    def __str__(self):
        return f"Solicitud #{self.pk} - {self.vecino}"


class Certificado(models.Model):

    solicitud = models.OneToOneField(
        SolicitudCertificado,
        on_delete=models.CASCADE,
        related_name="certificado",
    )

    fecha_emision = models.DateTimeField(
        auto_now_add=True
    )

    nombre_vecino = models.CharField(
        max_length=100,
    )

    apellido_vecino = models.CharField(
        max_length=100,
    )

    identificacion_vecino = models.CharField(
        max_length=30,
    )

    direccion_vecino = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return f"Certificado #{self.pk}"