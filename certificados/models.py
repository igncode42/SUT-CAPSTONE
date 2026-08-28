from django.db import models
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
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )

    def __str__(self):
        return f"Solicitud #{self.pk} - {self.vecino}"


class Certificado(models.Model):
    solicitud = models.OneToOneField(
        SolicitudCertificado,
        on_delete=models.CASCADE,
        related_name="certificado",
    )
    fecha_emision = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificado #{self.pk}"