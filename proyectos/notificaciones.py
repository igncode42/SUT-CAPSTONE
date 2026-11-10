from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import escape


def enviar_resolucion_proyecto(proyecto):
    destinatario = proyecto.vecino.usuario.email.strip()

    if not destinatario:
        return False

    estado = proyecto.get_estado_display()

    nombre = escape(
        proyecto.vecino.nombre
    )

    titulo = escape(
        proyecto.titulo
    )


    if estado == "Aprobado":

        color_estado = "#216e4e"

        titulo_estado = (
            "Proyecto aprobado"
        )

        detalle = (
            "Tu propuesta fue revisada por el personal "
            "autorizado y ha sido aprobada."
        )

    elif estado == "Rechazado":

        color_estado = "#b42318"

        titulo_estado = (
            "Proyecto rechazado"
        )

        detalle = (
            "Tu propuesta fue revisada por el personal "
            "autorizado y ha sido rechazada."
        )

    else:

        color_estado = "#627067"

        titulo_estado = (
            "Resolución de proyecto"
        )

        detalle = (
            "El estado de tu proyecto vecinal "
            "fue actualizado."
        )


    asunto = (
        f"Resolución de proyecto vecinal: "
        f"{proyecto.titulo}"
    )


    # ========================================================
    # VERSION TEXTO
    # Mantener para clientes de correo sin HTML y tests.
    # ========================================================

    mensaje_texto = (
        f"Hola {proyecto.vecino.nombre},\n\n"
        f"Tu proyecto vecinal \"{proyecto.titulo}\" "
        f"fue resuelto con estado: {estado}.\n\n"
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


            <!-- CABECERA -->

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


            <!-- CONTENIDO -->

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
                    Proyecto vecinal
                </p>


                <h1
                    style="
                        margin: 0 0 20px;
                        font-size: 24px;
                        line-height: 1.3;
                        color: #202923;
                    "
                >
                    {titulo_estado}
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
                    Tenemos una actualización sobre
                    tu proyecto vecinal.
                </p>


                <!-- RESUMEN -->

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
                            margin-bottom: 8px;
                            color: #627067;
                            font-size: 12px;
                            font-weight: bold;
                            text-transform: uppercase;
                        "
                    >
                        Proyecto
                    </div>

                    <div
                        style="
                            margin-bottom: 18px;
                            color: #202923;
                            font-size: 17px;
                            font-weight: bold;
                        "
                    >
                        {titulo}
                    </div>


                    <div
                        style="
                            margin-bottom: 8px;
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


            <!-- PIE -->

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