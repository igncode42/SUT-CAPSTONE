from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import (
    PerfilUsuarioForm,
    PerfilVecinoForm,
)

from .permisos import (
    es_miembro_junta,
    es_vecino,
    permiso_requerido,
    puede_gestionar_certificados,
    puede_gestionar_vecinos,
    puede_publicar_comunicaciones,
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

            "puede_gestionar_certificados": puede_gestionar_certificados(
                request.user
            ),

            "puede_publicar_comunicaciones": puede_publicar_comunicaciones(
                request.user
            ),

            "puede_gestionar_vecinos": puede_gestionar_vecinos(
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


@permiso_requerido(es_vecino)
def perfil(request):

    vecino = request.user.vecino

    if request.method == "POST":

        usuario_form = PerfilUsuarioForm(
            request.POST,
            instance=request.user,
        )

        vecino_form = PerfilVecinoForm(
            request.POST,
            instance=vecino,
        )

        if (
            usuario_form.is_valid()
            and vecino_form.is_valid()
        ):

            with transaction.atomic():

                usuario_form.save()
                vecino_form.save()

            messages.success(
                request,
                "Tus datos fueron actualizados correctamente.",
            )

            return redirect("perfil")

    else:

        usuario_form = PerfilUsuarioForm(
            instance=request.user,
        )

        vecino_form = PerfilVecinoForm(
            instance=vecino,
        )

    return render(
        request,
        "usuarios/perfil.html",
        {
            "usuario_form": usuario_form,
            "vecino_form": vecino_form,
            "vecino": vecino,
        },
    )