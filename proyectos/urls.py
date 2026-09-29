from django.urls import path

from .views import (
    crear_proyecto,
    mis_proyectos,
    proyectos_pendientes,
    resolver_proyecto,
)


app_name = "proyectos"


urlpatterns = [
    path(
        "crear/",
        crear_proyecto,
        name="crear",
    ),
    path(
        "mis-proyectos/",
        mis_proyectos,
        name="mis_proyectos",
    ),
    path(
        "pendientes/",
        proyectos_pendientes,
        name="pendientes",
    ),
    path(
        "<int:pk>/resolver/<str:decision>/",
        resolver_proyecto,
        name="resolver",
    ),
]
