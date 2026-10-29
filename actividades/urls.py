from django.urls import path

from . import views


app_name = "actividades"

urlpatterns = [
    path(
        "",
        views.actividades_disponibles,
        name="disponibles",
    ),
    path(
        "mis-actividades/",
        views.mis_actividades,
        name="mis_actividades",
    ),
    path(
        "<int:actividad_id>/inscribir/",
        views.inscribir_actividad,
        name="inscribir",
    ),
]