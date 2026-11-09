from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path(
        "",
        TemplateView.as_view(
            template_name="home.html",
        ),
        name="home",
    ),

    # Autenticación Django
    path(
        "cuentas/",
        include("django.contrib.auth.urls"),
    ),

    # Área personal
    path(
        "panel/",
        include("usuarios.urls"),
    ),

    # Módulos SUT
    path(
        "proyectos/",
        include("proyectos.urls"),
    ),
    path(
        "certificados/",
        include("certificados.urls"),
    ),
    path(
        "vecinos/",
        include("vecinos.urls"),
    ),
    path(
        "reservas/",
        include("reservas.urls"),
    ),
    path(
        "actividades/",
        include("actividades.urls"),
    ),
    path(
        "comunicaciones/",
        include("comunicaciones.urls"),
    ),

    # Administración Django
    path(
        "admin/",
        admin.site.urls,
    ),
]