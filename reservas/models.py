from django.db import models
from django.db.models import Q

from vecinos.models import Vecino


class Espacio(models.Model):
    nombre = models.CharField(
        max_length=150
    )

    descripcion = models.TextField(
        blank=True
    )

    activo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.nombre


class Reserva(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        CONFIRMADA = "CONFIRMADA", "Confirmada"
        CANCELADA = "CANCELADA", "Cancelada"

    vecino = models.ForeignKey(
        Vecino,
        on_delete=models.CASCADE,
        related_name="reservas",
    )

    espacio = models.ForeignKey(
        Espacio,
        on_delete=models.CASCADE,
        related_name="reservas",
    )

    fecha = models.DateField()

    hora_inicio = models.TimeField()

    hora_fin = models.TimeField()

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.CONFIRMADA,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(
                    estado__in=[
                        "PENDIENTE",
                        "CONFIRMADA",
                        "CANCELADA",
                    ]
                ),
                name="reserva_estado_valido",
            ),
            models.CheckConstraint(
                condition=Q(
                    hora_inicio__lt=models.F("hora_fin")
                ),
                name="reserva_hora_inicio_menor_hora_fin",
            ),
        ]

    def __str__(self):
        return f"{self.espacio} - {self.fecha}"