from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from usuarios.permisos import es_vecino, permiso_requerido

from .models import SolicitudCertificado


@permiso_requerido(es_vecino)
@require_POST
def solicitar_certificado(request):

    SolicitudCertificado.objects.create(
        vecino=request.user.vecino,
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
