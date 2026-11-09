from django.urls import path

from . import views


app_name = "comunicaciones"


urlpatterns = [
    path(
        "",
        views.comunicaciones_inicio,
        name="inicio",
    ),

    # Noticias
    path(
        "noticias/nueva/",
        views.publicar_noticia,
        name="publicar_noticia",
    ),
    path(
        "noticias/<int:pk>/editar/",
        views.editar_noticia,
        name="editar_noticia",
    ),
    path(
        "noticias/<int:pk>/eliminar/",
        views.eliminar_noticia,
        name="eliminar_noticia",
    ),

    # Avisos
    path(
        "avisos/nuevo/",
        views.publicar_aviso,
        name="publicar_aviso",
    ),
    path(
        "avisos/<int:pk>/editar/",
        views.editar_aviso,
        name="editar_aviso",
    ),
    path(
        "avisos/<int:pk>/eliminar/",
        views.eliminar_aviso,
        name="eliminar_aviso",
    ),
]