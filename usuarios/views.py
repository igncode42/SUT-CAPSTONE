from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .permisos import (
    es_miembro_junta,
    es_vecino,
    permiso_requerido,
    puede_resolver_proyectos,
)


@login_required
def panel(request):
    return render(
        request,
        "usuarios/panel.html",
        {
            "es_vecino": es_vecino(request.user),
            "es_miembro_junta": es_miembro_junta(request.user),
            "puede_resolver_proyectos": puede_resolver_proyectos(
                request.user
            ),
        },
    )


@permiso_requerido(es_miembro_junta)
def panel_miembro(request):
    return render(
        request,
        "usuarios/panel_miembro.html",
    )
