from django.db import models
from django.db.models import Q

from vecinos.models import Vecino


class ProyectoVecinal(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente de revisión"
        APROBADO = "APROBADO", "Aprobado"
        RECHAZADO = "RECHAZADO", "Rechazado"

    vecino = models.ForeignKey(
        Vecino,
        on_delete=models.CASCADE,
        related_name="proyectos",
    )

    titulo = models.CharField(
        max_length=200
    )

    descripcion = models.TextField()

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )

    fecha_postulacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(
                    estado__in=[
                        "PENDIENTE",
                        "APROBADO",
                        "RECHAZADO",
                    ]
                ),
                name="proyecto_estado_valido",
            ),
        ]

    def __str__(self):
        return self.titulo