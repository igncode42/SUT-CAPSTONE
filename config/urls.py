from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="home.html"),
        name="home",
    ),
    path(
        "cuentas/",
        include("django.contrib.auth.urls"),
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
    path("admin/", admin.site.urls),
]
