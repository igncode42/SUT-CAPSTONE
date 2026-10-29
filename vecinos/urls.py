from django.urls import path

from . import views


app_name = "vecinos"

urlpatterns = [
    path(
        "registro/",
        views.registro_vecino,
        name="registro",
    ),
]