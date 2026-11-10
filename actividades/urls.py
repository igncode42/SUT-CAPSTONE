from django.urls import path

from . import views


app_name = "actividades"

urlpatterns = [
    # ========================================================
    # VECINOS
    # ========================================================

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

    # ========================================================
    # GESTION ADMINISTRATIVA
    # ========================================================

    path(
        "gestion/",
        views.gestion_actividades,
        name="gestion",
    ),
    path(
        "gestion/crear/",
        views.crear_actividad,
        name="crear",
    ),
    path(
        "gestion/<int:actividad_id>/editar/",
        views.editar_actividad,
        name="editar",
    ),
    path(
        "gestion/<int:actividad_id>/eliminar/",
        views.eliminar_actividad,
        name="eliminar",
    ),
]