from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from usuarios.permisos import (
    es_vecino,
    permiso_requerido,
    puede_gestionar_certificados,
)

from .models import (
    Certificado,
    SolicitudCertificado,
)


@permiso_requerido(es_vecino)
@require_POST
def solicitar_certificado(request):
    vecino = request.user.vecino

    solicitud_activa = SolicitudCertificado.objects.filter(
        vecino=vecino,
        estado__in=[
            SolicitudCertificado.Estado.PENDIENTE,
            SolicitudCertificado.Estado.APROBADA,
        ],
    ).exists()

    if solicitud_activa:
        messages.warning(
            request,
            "Ya tienes una solicitud de certificado en proceso.",
        )

        return redirect(
            "certificados:mis_solicitudes"
        )

    SolicitudCertificado.objects.create(
        vecino=vecino,
    )

    messages.success(
        request,
        "Solicitud de certificado creada correctamente.",
    )

    return redirect(
        "certificados:mis_solicitudes"
    )


@permiso_requerido(es_vecino)
def mis_solicitudes(request):

    solicitudes = (
        SolicitudCertificado.objects
        .filter(vecino=request.user.vecino)
        .order_by("-fecha_solicitud")
    )

    return render(
        request,
        "certificados/mis_solicitudes.html",
        {
            "solicitudes": solicitudes,
        },
    )


@permiso_requerido(puede_gestionar_certificados)
def solicitudes_pendientes(request):

    solicitudes = (
        SolicitudCertificado.objects
        .filter(
            estado=SolicitudCertificado.Estado.PENDIENTE
        )
        .select_related(
            "vecino",
            "vecino__usuario",
        )
        .order_by("fecha_solicitud")
    )

    return render(
        request,
        "certificados/pendientes.html",
        {
            "solicitudes": solicitudes,
        },
    )


@permiso_requerido(puede_gestionar_certificados)
@require_POST
def resolver_solicitud(request, pk, decision):

    solicitud = get_object_or_404(
        SolicitudCertificado,
        pk=pk,
    )

    if solicitud.estado != SolicitudCertificado.Estado.PENDIENTE:

        return HttpResponseBadRequest(
            "La solicitud ya fue resuelta."
        )

    if decision == "aprobar":

        solicitud.estado = SolicitudCertificado.Estado.APROBADA

    elif decision == "rechazar":

        solicitud.estado = SolicitudCertificado.Estado.RECHAZADA

    else:

        return HttpResponseBadRequest(
            "Decisión no válida."
        )

    solicitud.save(
        update_fields=["estado"]
    )

    return redirect(
        "certificados:pendientes"
    )


@permiso_requerido(puede_gestionar_certificados)
@require_POST
def emitir_certificado(request, pk):

    with transaction.atomic():

        solicitud = get_object_or_404(
            SolicitudCertificado.objects.select_for_update(),
            pk=pk,
        )

        if solicitud.estado != SolicitudCertificado.Estado.APROBADA:

            return HttpResponseBadRequest(
                "Sólo una solicitud aprobada puede emitirse."
            )

        if hasattr(solicitud, "certificado"):

            return HttpResponseBadRequest(
                "La solicitud ya posee certificado."
            )

        Certificado.objects.create(
            solicitud=solicitud,
        )

        solicitud.estado = SolicitudCertificado.Estado.EMITIDA

        solicitud.save(
            update_fields=["estado"]
        )

    return redirect(
        "certificados:gestion"
    )


@permiso_requerido(puede_gestionar_certificados)
def gestion_certificados(request):

    solicitudes = (
        SolicitudCertificado.objects
        .select_related(
            "vecino",
            "vecino__usuario",
        )
        .order_by("-fecha_solicitud")
    )

    return render(
        request,
        "certificados/gestion.html",
        {
            "solicitudes": solicitudes,
        },
    )


@permiso_requerido(es_vecino)
def ver_certificado(request, pk):
    solicitud = get_object_or_404(
        SolicitudCertificado.objects.select_related(
            "vecino",
            "vecino__usuario",
        ),
        pk=pk,
        vecino=request.user.vecino,
        estado=SolicitudCertificado.Estado.EMITIDA,
    )

    if not hasattr(solicitud, "certificado"):
        return HttpResponseBadRequest(
            "La solicitud no posee un certificado emitido."
        )

    return render(
        request,
        "certificados/ver_certificado.html",
        {
            "solicitud": solicitud,
            "certificado": solicitud.certificado,
        },
    )
