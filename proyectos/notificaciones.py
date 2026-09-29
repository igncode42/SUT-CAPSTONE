from django.conf import settings
from django.core.mail import send_mail


def enviar_resolucion_proyecto(proyecto):

    destinatario = proyecto.vecino.usuario.email.strip()

    if not destinatario:
        return False

    estado = proyecto.get_estado_display()

    asunto = (
        f"Resolución de proyecto vecinal: "
        f"{proyecto.titulo}"
    )

    mensaje = (
        f"Hola {proyecto.vecino.nombre},\n\n"
        f"Tu proyecto vecinal \"{proyecto.titulo}\" "
        f"fue resuelto con estado: {estado}.\n\n"
        "Sistema Unidad Territorial (SUT)"
    )

    send_mail(
        subject=asunto,
        message=mensaje,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[destinatario],
        fail_silently=False,
    )

    return True
