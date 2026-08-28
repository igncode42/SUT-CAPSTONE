from django.db import models
from vecinos.models import Vecino


class Actividad(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField()
    cupo_maximo = models.PositiveIntegerField()

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
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["vecino", "actividad"],
                name="unique_vecino_actividad",
            )
        ]

    def __str__(self):
        return f"{self.vecino} - {self.actividad}"