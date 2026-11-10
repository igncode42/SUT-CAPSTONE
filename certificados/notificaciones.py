from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import escape

from .models import SolicitudCertificado
from .pdf import (
    generar_certificado_pdf,
    nombre_archivo_certificado,
)


def _obtener_destinatario(solicitud):
    return solicitud.vecino.usuario.email.strip()


def enviar_resolucion_certificado(solicitud):
    """
    Notifica por correo la aprobación o rechazo
    de una solicitud de certificado.
    """

    destinatario = _obtener_destinatario(
        solicitud
    )

    if not destinatario:
        return False


    if solicitud.estado == SolicitudCertificado.Estado.APROBADA:

        estado = "Aprobada"

        asunto = (
            "[SUT] Solicitud de certificado aprobada"
        )

        resumen = (
            "Tu solicitud de certificado de residencia "
            "fue aprobada."
        )

        detalle = (
            "La solicitud fue revisada correctamente y "
            "se encuentra pendiente de emisión."
        )

        color_estado = "#216e4e"


    elif solicitud.estado == SolicitudCertificado.Estado.RECHAZADA:

        estado = "Rechazada"

        asunto = (
            "[SUT] Solicitud de certificado rechazada"
        )

        resumen = (
            "Tu solicitud de certificado de residencia "
            "fue rechazada."
        )

        detalle = (
            "La solicitud fue revisada por el personal "
            "autorizado del Sistema Unidad Territorial."
        )

        color_estado = "#b42318"


    else:

        raise ValueError(
            "Sólo se pueden notificar solicitudes "
            "aprobadas o rechazadas."
        )


    nombre = escape(
        solicitud.vecino.nombre
    )


    # ========================================================
    # VERSION TEXTO
    # ========================================================

    mensaje_texto = (
        f"Hola {solicitud.vecino.nombre},\n\n"
        f"{resumen}\n\n"
        f"Solicitud: #{solicitud.pk}\n"
        f"Estado: {estado}\n\n"
        f"{detalle}\n\n"
        "Puedes consultar el estado actualizado desde "
        "tu cuenta en el Sistema Unidad Territorial.\n\n"
        "Sistema Unidad Territorial (SUT)"
    )


    # ========================================================
    # VERSION HTML
    # ========================================================

    mensaje_html = f"""
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
</head>

<body
    style="
        margin: 0;
        padding: 0;
        background-color: #f6f4ef;
        font-family: Arial, Helvetica, sans-serif;
        color: #202923;
    "
>

    <div
        style="
            max-width: 620px;
            margin: 0 auto;
            padding: 32px 16px;
        "
    >

        <div
            style="
                background-color: #ffffff;
                border: 1px solid #d9e1da;
                border-radius: 14px;
                overflow: hidden;
            "
        >

            <div
                style="
                    background-color: #2f624a;
                    padding: 24px 30px;
                    color: #ffffff;
                "
            >

                <div
                    style="
                        font-size: 13px;
                        font-weight: bold;
                        letter-spacing: 1px;
                    "
                >
                    SUT
                </div>

                <div
                    style="
                        margin-top: 4px;
                        font-size: 18px;
                        font-weight: bold;
                    "
                >
                    Sistema Unidad Territorial
                </div>

            </div>


            <div
                style="
                    padding: 32px 30px;
                "
            >

                <p
                    style="
                        margin: 0 0 8px;
                        color: #627067;
                        font-size: 13px;
                        font-weight: bold;
                        text-transform: uppercase;
                    "
                >
                    Certificado de residencia
                </p>


                <h1
                    style="
                        margin: 0 0 20px;
                        font-size: 24px;
                        line-height: 1.3;
                        color: #202923;
                    "
                >
                    Solicitud {estado.lower()}
                </h1>


                <p
                    style="
                        margin: 0 0 18px;
                        font-size: 16px;
                        line-height: 1.6;
                    "
                >
                    Hola <strong>{nombre}</strong>,
                </p>


                <p
                    style="
                        margin: 0 0 24px;
                        font-size: 16px;
                        line-height: 1.6;
                    "
                >
                    {resumen}
                </p>


                <div
                    style="
                        margin: 0 0 24px;
                        padding: 18px 20px;
                        background-color: #f7faf8;
                        border: 1px solid #d9e1da;
                        border-radius: 10px;
                    "
                >

                    <div
                        style="
                            margin-bottom: 10px;
                            color: #627067;
                            font-size: 12px;
                            font-weight: bold;
                            text-transform: uppercase;
                        "
                    >
                        Solicitud
                    </div>

                    <div
                        style="
                            margin-bottom: 18px;
                            font-size: 17px;
                            font-weight: bold;
                        "
                    >
                        #{solicitud.pk}
                    </div>


                    <div
                        style="
                            margin-bottom: 10px;
                            color: #627067;
                            font-size: 12px;
                            font-weight: bold;
                            text-transform: uppercase;
                        "
                    >
                        Estado
                    </div>

                    <div
                        style="
                            color: {color_estado};
                            font-size: 17px;
                            font-weight: bold;
                        "
                    >
                        {estado}
                    </div>

                </div>


                <p
                    style="
                        margin: 0 0 18px;
                        color: #627067;
                        font-size: 15px;
                        line-height: 1.6;
                    "
                >
                    {detalle}
                </p>


                <p
                    style="
                        margin: 0;
                        color: #627067;
                        font-size: 14px;
                        line-height: 1.6;
                    "
                >
                    Puedes consultar el estado actualizado
                    desde tu cuenta en el Sistema Unidad Territorial.
                </p>

            </div>


            <div
                style="
                    padding: 20px 30px;
                    background-color: #edf4ee;
                    border-top: 1px solid #d9e1da;
                    color: #627067;
                    font-size: 12px;
                    line-height: 1.5;
                "
            >
                Sistema Unidad Territorial ·
                Notificación generada automáticamente
            </div>

        </div>

    </div>

</body>
</html>
"""


    correo = EmailMultiAlternatives(
        subject=asunto,
        body=mensaje_texto,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[destinatario],
    )

    correo.attach_alternative(
        mensaje_html,
        "text/html",
    )

    enviados = correo.send(
        fail_silently=False
    )

    return enviados == 1


def enviar_certificado_emitido(certificado):
    """
    Envía al vecino el certificado emitido
    como archivo PDF adjunto.
    """

    solicitud = certificado.solicitud

    destinatario = _obtener_destinatario(
        solicitud
    )

    if not destinatario:
        return False


    nombre = escape(
        certificado.nombre_vecino
    )

    nombre_archivo = nombre_archivo_certificado(
        certificado
    )

    pdf = generar_certificado_pdf(
        certificado
    )


    asunto = (
        "[SUT] Tu certificado de residencia "
        "fue emitido"
    )


    # ========================================================
    # VERSION TEXTO
    # ========================================================

    mensaje_texto = (
        f"Hola {certificado.nombre_vecino},\n\n"
        "Tu certificado de residencia fue emitido "
        "correctamente.\n\n"
        f"Solicitud: #{solicitud.pk}\n"
        f"Certificado: #{certificado.pk}\n"
        "Estado: Emitido\n\n"
        "Adjuntamos tu certificado de residencia "
        "en formato PDF.\n\n"
        "También puedes consultarlo y descargarlo "
        "desde tu cuenta en el Sistema Unidad Territorial.\n\n"
        "Sistema Unidad Territorial (SUT)"
    )


    # ========================================================
    # VERSION HTML
    # ========================================================

    mensaje_html = f"""
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
</head>

<body
    style="
        margin: 0;
        padding: 0;
        background-color: #f6f4ef;
        font-family: Arial, Helvetica, sans-serif;
        color: #202923;
    "
>

    <div
        style="
            max-width: 620px;
            margin: 0 auto;
            padding: 32px 16px;
        "
    >

        <div
            style="
                background-color: #ffffff;
                border: 1px solid #d9e1da;
                border-radius: 14px;
                overflow: hidden;
            "
        >

            <div
                style="
                    background-color: #2f624a;
                    padding: 24px 30px;
                    color: #ffffff;
                "
            >

                <div
                    style="
                        font-size: 13px;
                        font-weight: bold;
                        letter-spacing: 1px;
                    "
                >
                    SUT
                </div>

                <div
                    style="
                        margin-top: 4px;
                        font-size: 18px;
                        font-weight: bold;
                    "
                >
                    Sistema Unidad Territorial
                </div>

            </div>


            <div
                style="
                    padding: 32px 30px;
                "
            >

                <p
                    style="
                        margin: 0 0 8px;
                        color: #216e4e;
                        font-size: 13px;
                        font-weight: bold;
                        text-transform: uppercase;
                    "
                >
                    Documento emitido
                </p>


                <h1
                    style="
                        margin: 0 0 20px;
                        font-size: 24px;
                        line-height: 1.3;
                        color: #202923;
                    "
                >
                    Tu certificado está listo
                </h1>


                <p
                    style="
                        margin: 0 0 18px;
                        font-size: 16px;
                        line-height: 1.6;
                    "
                >
                    Hola <strong>{nombre}</strong>,
                </p>


                <p
                    style="
                        margin: 0 0 24px;
                        font-size: 16px;
                        line-height: 1.6;
                    "
                >
                    Tu certificado de residencia fue
                    emitido correctamente.
                </p>


                <div
                    style="
                        margin: 0 0 24px;
                        padding: 18px 20px;
                        background-color: #edf4ee;
                        border: 1px solid #bfd0c3;
                        border-radius: 10px;
                    "
                >

                    <div
                        style="
                            margin-bottom: 7px;
                            color: #627067;
                            font-size: 12px;
                            font-weight: bold;
                            text-transform: uppercase;
                        "
                    >
                        Solicitud
                    </div>

                    <div
                        style="
                            margin-bottom: 17px;
                            font-size: 16px;
                            font-weight: bold;
                        "
                    >
                        #{solicitud.pk}
                    </div>


                    <div
                        style="
                            margin-bottom: 7px;
                            color: #627067;
                            font-size: 12px;
                            font-weight: bold;
                            text-transform: uppercase;
                        "
                    >
                        Estado
                    </div>

                    <div
                        style="
                            color: #216e4e;
                            font-size: 17px;
                            font-weight: bold;
                        "
                    >
                        Emitido
                    </div>

                </div>


                <p
                    style="
                        margin: 0 0 16px;
                        color: #202923;
                        font-size: 15px;
                        line-height: 1.6;
                    "
                >
                    Encontrarás tu certificado adjunto
                    a este correo en formato PDF.
                </p>


                <p
                    style="
                        margin: 0;
                        color: #627067;
                        font-size: 14px;
                        line-height: 1.6;
                    "
                >
                    También puedes consultarlo y descargarlo
                    desde tu cuenta en el Sistema Unidad Territorial.
                </p>

            </div>


            <div
                style="
                    padding: 20px 30px;
                    background-color: #edf4ee;
                    border-top: 1px solid #d9e1da;
                    color: #627067;
                    font-size: 12px;
                    line-height: 1.5;
                "
            >
                Sistema Unidad Territorial ·
                Documento generado electrónicamente
            </div>

        </div>

    </div>

</body>
</html>
"""


    correo = EmailMultiAlternatives(
        subject=asunto,
        body=mensaje_texto,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[destinatario],
    )

    correo.attach_alternative(
        mensaje_html,
        "text/html",
    )

    correo.attach(
        nombre_archivo,
        pdf,
        "application/pdf",
    )

    enviados = correo.send(
        fail_silently=False
    )

    return enviados == 1