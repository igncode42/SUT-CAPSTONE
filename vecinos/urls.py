from django.urls import path

from . import views


app_name = "vecinos"

urlpatterns = [
    path(
        "registro/",
        views.registro_vecino,
        name="registro",
    ),
    path(
        "gestion/",
        views.gestion_vecinos,
        name="gestion",
    ),
    path(
        "<int:vecino_id>/miembro/",
        views.actualizar_miembro,
        name="actualizar_miembro",
    ),
]