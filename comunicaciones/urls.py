from django.urls import path

from . import views


app_name = "comunicaciones"

urlpatterns = [
    path(
        "",
        views.comunicaciones_inicio,
        name="inicio",
    ),
    path(
        "noticias/nueva/",
        views.publicar_noticia,
        name="publicar_noticia",
    ),
    path(
        "avisos/nuevo/",
        views.publicar_aviso,
        name="publicar_aviso",
    ),
]