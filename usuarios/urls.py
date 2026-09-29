from django.urls import path

from .views import panel, panel_miembro


urlpatterns = [
    path("", panel, name="panel"),
    path(
        "miembro-junta/",
        panel_miembro,
        name="panel_miembro",
    ),
]
