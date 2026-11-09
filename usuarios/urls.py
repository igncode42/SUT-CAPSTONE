from django.urls import path

from .views import (
    panel,
    panel_miembro,
    perfil,
)


urlpatterns = [
    path(
        "",
        panel,
        name="panel",
    ),
    path(
        "perfil/",
        perfil,
        name="perfil",
    ),
    path(
        "miembro-junta/",
        panel_miembro,
        name="panel_miembro",
    ),
]