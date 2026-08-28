from django.conf import settings
from django.db import models


class Vecino(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vecino",
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=30, unique=True)
    direccion = models.CharField(max_length=255)
    miembro_junta = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"