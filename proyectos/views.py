import logging

from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from usuarios.permisos import (
    es_miembro_junta,
    permiso_requerido,
    puede_resolver_proyectos,
)

from .forms import ProyectoVecinalForm
from .models import ProyectoVecinal
from .notificaciones import enviar_resolucion_proyecto


logger = logging.getLogger(__name__)


@permiso_requerido(es_miembro_junta)
def crear_proyecto(request):

    if request.method == "POST":

        form = ProyectoVecinalForm(request.POST)

        if form.is_valid():

            proyecto = form.save(commit=False)

            proyecto.vecino = request.user.vecino
            proyecto.estado = ProyectoVecinal.Estado.PENDIENTE

            proyecto.save()

            return redirect("proyectos:mis_proyectos")

    else:
        form = ProyectoVecinalForm()

    return render(
        request,
        "proyectos/crear.html",
        {
            "form": form,
        },
    )


@permiso_requerido(es_miembro_junta)
def mis_proyectos(request):

    proyectos = (
        ProyectoVecinal.objects
        .filter(vecino=request.user.vecino)
        .order_by("-fecha_postulacion")
    )

    return render(
        request,
        "proyectos/mis_proyectos.html",
        {
            "proyectos": proyectos,
        },
    )


@permiso_requerido(puede_resolver_proyectos)
def proyectos_pendientes(request):

    proyectos = (
        ProyectoVecinal.objects
        .filter(estado=ProyectoVecinal.Estado.PENDIENTE)
        .select_related(
            "vecino",
            "vecino__usuario",
        )
        .order_by("fecha_postulacion")
    )

    return render(
        request,
        "proyectos/pendientes.html",
        {
            "proyectos": proyectos,
        },
    )


@permiso_requerido(puede_resolver_proyectos)
@require_POST
def resolver_proyecto(request, pk, decision):

    if decision not in {"aprobar", "rechazar"}:

        return HttpResponseBadRequest(
            "Decisión no válida."
        )

    with transaction.atomic():

        proyecto = get_object_or_404(
            ProyectoVecinal.objects
            .select_for_update()
            .select_related(
                "vecino",
                "vecino__usuario",
            ),
            pk=pk,
        )

        if proyecto.estado != ProyectoVecinal.Estado.PENDIENTE:

            return HttpResponseBadRequest(
                "El proyecto ya fue resuelto."
            )

        if decision == "aprobar":
            proyecto.estado = ProyectoVecinal.Estado.APROBADO

        else:
            proyecto.estado = ProyectoVecinal.Estado.RECHAZADO

        proyecto.save(
            update_fields=["estado"]
        )

    try:

        notificacion_enviada = enviar_resolucion_proyecto(
            proyecto
        )

    except Exception:

        logger.exception(
            "Error al enviar la notificación del proyecto %s.",
            proyecto.pk,
        )

        notificacion_enviada = False

    if notificacion_enviada:

        messages.success(
            request,
            "Resolución guardada y notificación enviada por correo.",
        )

    else:

        messages.warning(
            request,
            "Resolución guardada, pero la notificación por correo no pudo enviarse.",
        )

    return redirect(
        "proyectos:pendientes"
    )