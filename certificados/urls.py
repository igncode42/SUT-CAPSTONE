from django.urls import path

from .views import (
    emitir_certificado,
    gestion_certificados,
    mis_solicitudes,
    resolver_solicitud,
    solicitudes_pendientes,
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
    path(
        "pendientes/",
        solicitudes_pendientes,
        name="pendientes",
    ),
    path(
        "gestion/",
        gestion_certificados,
        name="gestion",
    ),
    path(
        "<int:pk>/resolver/<str:decision>/",
        resolver_solicitud,
        name="resolver",
    ),
    path(
        "<int:pk>/emitir/",
        emitir_certificado,
        name="emitir",
    ),
]
