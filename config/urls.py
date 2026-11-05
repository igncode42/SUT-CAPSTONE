from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path(
        "",
        TemplateView.as_view(
            template_name="home.html"
        ),
        name="home",
    ),

    path(
        "cuentas/login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),

    path(
        "cuentas/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    path(
        "panel/",
        include("usuarios.urls"),
    ),

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

    path(
        "admin/",
        admin.site.urls,
    ),
]