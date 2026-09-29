from django.urls import path

from .views import crear_proyecto, mis_proyectos


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
]
