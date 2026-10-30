from django.urls import path

from . import views


app_name = "comunicaciones"

urlpatterns = [
    path(
        "",
        views.comunicaciones_inicio,
        name="inicio",
    ),
]