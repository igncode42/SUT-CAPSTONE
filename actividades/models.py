from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from vecinos.models import Vecino


class Actividad(models.Model):

    nombre = models.CharField(
        max_length=150
    )

    descripcion = models.TextField(
        blank=True
    )

    fecha = models.DateTimeField()

    cupo_maximo = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(
                    cupo_maximo__gte=1
                ),
                name="actividad_cupo_maximo_minimo_1",
            ),
        ]

    def __str__(self):
        return self.nombre


class InscripcionActividad(models.Model):

    vecino = models.ForeignKey(
        Vecino,
        on_delete=models.CASCADE,
        related_name="inscripciones_actividad",
    )

    actividad = models.ForeignKey(
        Actividad,
        on_delete=models.CASCADE,
        related_name="inscripciones",
    )

    fecha_inscripcion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "vecino",
                    "actividad",
                ],
                name="unique_vecino_actividad",
            ),
        ]

    def __str__(self):
        return f"{self.vecino} - {self.actividad}"