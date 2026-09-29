from django.urls import path

from .views import (
    mis_solicitudes,
    solicitar_certificado,
)


app_name = "certificados"


urlpatterns = [
    path(
        "mis-solicitudes/",
        mis_solicitudes,
        name="mis_solicitudes",
    ),
    path(
        "solicitar/",
        solicitar_certificado,
        name="solicitar",
    ),
]
