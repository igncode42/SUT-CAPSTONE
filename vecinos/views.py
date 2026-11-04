from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from usuarios.permisos import (
    puede_gestionar_vecinos,
    permiso_requerido,
)

from .forms import RegistroVecinoForm
from .models import Vecino


def registro_vecino(request):
    if request.method == "POST":
        form = RegistroVecinoForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                usuario = form.save()

                Vecino.objects.create(
                    usuario=usuario,
                    nombre=form.cleaned_data["nombre"],
                    apellido=form.cleaned_data["apellido"],
                    identificacion=form.cleaned_data["identificacion"],
                    direccion=form.cleaned_data["direccion"],
                )

            messages.success(
                request,
                "Registro completado correctamente. Ya puedes iniciar sesión.",
            )

            return redirect("login")

    else:
        form = RegistroVecinoForm()

    return render(
        request,
        "vecinos/registro.html",
        {
            "form": form,
        },
    )


@permiso_requerido(puede_gestionar_vecinos)
def gestion_vecinos(request):
    vecinos = (
        Vecino.objects
        .select_related("usuario")
        .order_by("apellido", "nombre")
    )

    return render(
        request,
        "vecinos/gestion.html",
        {
            "vecinos": vecinos,
        },
    )


@require_POST
@permiso_requerido(puede_gestionar_vecinos)
def actualizar_miembro(request, vecino_id):
    vecino = get_object_or_404(
        Vecino,
        pk=vecino_id,
    )

    nuevo_estado = request.POST.get("miembro_junta") == "true"

    vecino.miembro_junta = nuevo_estado
    vecino.save(
        update_fields=["miembro_junta"],
    )

    if nuevo_estado:
        messages.success(
            request,
            f"{vecino.nombre} {vecino.apellido} ahora es miembro de junta.",
        )
    else:
        messages.success(
            request,
            f"{vecino.nombre} {vecino.apellido} dejó de ser miembro de junta.",
        )

    return redirect("vecinos:gestion")