from django.shortcuts import render

from .models import Aviso, Noticia


def comunicaciones_inicio(request):
    noticias = (
        Noticia.objects.select_related("usuario")
        .order_by("-fecha_publicacion")
    )

    avisos = (
        Aviso.objects.select_related("usuario")
        .order_by("-fecha_publicacion")
    )

    return render(
        request,
        "comunicaciones/inicio.html",
        {
            "noticias": noticias,
            "avisos": avisos,
        },
    )