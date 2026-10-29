from django.urls import path

from . import views


app_name = "reservas"

urlpatterns = [
    path(
        "",
        views.mis_reservas,
        name="mis_reservas",
    ),
    path(
        "nueva/",
        views.crear_reserva,
        name="crear",
    ),
]