from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from usuarios.models import Rol
from vecinos.models import Vecino

from .models import (
    Certificado,
    SolicitudCertificado,
)
from .pdf import (
    generar_certificado_pdf,
    nombre_archivo_certificado,
)


Usuario = get_user_model()


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
)
class DocumentoNotificacionCertificadoTests(TestCase):

    def crear_vecino(
        self,
        username="vecino_certificado",
        email="vecino@example.com",
    ):

        usuario = Usuario.objects.create_user(
            username=username,
            password="ClaveSegura123!",
            email=email,
        )

        vecino = Vecino.objects.create(
            usuario=usuario,
            nombre="Nombre",
            apellido="Prueba",
            identificacion=f"ID-{username}",
            direccion="Dirección de prueba",
        )

        return usuario, vecino


    def crear_directiva(self):

        rol = Rol.objects.create(
            nombre="Directiva"
        )

        return Usuario.objects.create_user(
            username="directiva_certificados",
            password="ClaveSegura123!",
            email="directiva@example.com",
            rol=rol,
        )


    def crear_solicitud(
        self,
        vecino,
        estado=SolicitudCertificado.Estado.PENDIENTE,
    ):

        return SolicitudCertificado.objects.create(
            vecino=vecino,
            estado=estado,
        )


    def crear_certificado(
        self,
        solicitud,
    ):

        vecino = solicitud.vecino

        return Certificado.objects.create(
            solicitud=solicitud,
            nombre_vecino=vecino.nombre,
            apellido_vecino=vecino.apellido,
            identificacion_vecino=vecino.identificacion,
            direccion_vecino=vecino.direccion,
        )


    def login(
        self,
        usuario,
    ):

        return self.client.login(
            username=usuario.username,
            password="ClaveSegura123!",
        )


    # ========================================================
    # PDF
    # ========================================================

    def test_generar_certificado_pdf_retorna_pdf_valido(self):

        _, vecino = self.crear_vecino()

        solicitud = self.crear_solicitud(
            vecino,
            estado=SolicitudCertificado.Estado.EMITIDA,
        )

        certificado = self.crear_certificado(
            solicitud
        )

        pdf = generar_certificado_pdf(
            certificado
        )

        self.assertIsInstance(
            pdf,
            bytes,
        )

        self.assertTrue(
            pdf.startswith(b"%PDF-")
        )

        self.assertGreater(
            len(pdf),
            1000,
        )


    def test_nombre_archivo_pdf_es_predecible(self):

        _, vecino = self.crear_vecino()

        solicitud = self.crear_solicitud(
            vecino,
            estado=SolicitudCertificado.Estado.EMITIDA,
        )

        certificado = self.crear_certificado(
            solicitud
        )

        nombre = nombre_archivo_certificado(
            certificado
        )

        self.assertEqual(
            nombre,
            (
                "certificado-residencia-"
                f"SUT-CR-{certificado.pk:06d}.pdf"
            ),
        )


    # ========================================================
    # DESCARGA
    # ========================================================

    def test_vecino_puede_descargar_su_certificado(self):

        usuario, vecino = self.crear_vecino()

        solicitud = self.crear_solicitud(
            vecino,
            estado=SolicitudCertificado.Estado.EMITIDA,
        )

        certificado = self.crear_certificado(
            solicitud
        )

        self.login(
            usuario
        )

        response = self.client.get(
            reverse(
                "certificados:descargar",
                args=[solicitud.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response["Content-Type"],
            "application/pdf",
        )

        self.assertIn(
            nombre_archivo_certificado(certificado),
            response["Content-Disposition"],
        )

        self.assertTrue(
            response.content.startswith(
                b"%PDF-"
            )
        )

        self.assertEqual(
            response["Cache-Control"],
            "private, no-store",
        )


    def test_vecino_no_puede_descargar_certificado_de_otro(self):

        usuario_a, _ = self.crear_vecino(
            username="vecino_a",
            email="vecino_a@example.com",
        )

        _, vecino_b = self.crear_vecino(
            username="vecino_b",
            email="vecino_b@example.com",
        )

        solicitud_b = self.crear_solicitud(
            vecino_b,
            estado=SolicitudCertificado.Estado.EMITIDA,
        )

        self.crear_certificado(
            solicitud_b
        )

        self.login(
            usuario_a
        )

        response = self.client.get(
            reverse(
                "certificados:descargar",
                args=[solicitud_b.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )


    # ========================================================
    # CORREO DE RESOLUCION
    # ========================================================

    def test_aprobar_solicitud_envia_correo(self):

        _, vecino = self.crear_vecino(
            email="aprobado@example.com",
        )

        solicitud = self.crear_solicitud(
            vecino
        )

        directiva = self.crear_directiva()

        self.login(
            directiva
        )

        response = self.client.post(
            reverse(
                "certificados:resolver",
                args=[
                    solicitud.pk,
                    "aprobar",
                ],
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "certificados:pendientes"
            ),
        )

        solicitud.refresh_from_db()

        self.assertEqual(
            solicitud.estado,
            SolicitudCertificado.Estado.APROBADA,
        )

        self.assertEqual(
            len(mail.outbox),
            1,
        )

        correo = mail.outbox[0]

        self.assertEqual(
            correo.to,
            ["aprobado@example.com"],
        )

        self.assertIn(
            "aprobada",
            correo.subject.lower(),
        )

        self.assertEqual(
            len(correo.alternatives),
            1,
        )

        self.assertEqual(
            correo.alternatives[0].mimetype,
            "text/html",
        )


    def test_rechazar_solicitud_envia_correo(self):

        _, vecino = self.crear_vecino(
            email="rechazado@example.com",
        )

        solicitud = self.crear_solicitud(
            vecino
        )

        directiva = self.crear_directiva()

        self.login(
            directiva
        )

        response = self.client.post(
            reverse(
                "certificados:resolver",
                args=[
                    solicitud.pk,
                    "rechazar",
                ],
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "certificados:pendientes"
            ),
        )

        solicitud.refresh_from_db()

        self.assertEqual(
            solicitud.estado,
            SolicitudCertificado.Estado.RECHAZADA,
        )

        self.assertEqual(
            len(mail.outbox),
            1,
        )

        correo = mail.outbox[0]

        self.assertEqual(
            correo.to,
            ["rechazado@example.com"],
        )

        self.assertIn(
            "rechazada",
            correo.subject.lower(),
        )


    # ========================================================
    # EMISION + PDF POR EMAIL
    # ========================================================

    def test_emitir_certificado_envia_pdf_adjunto(self):

        _, vecino = self.crear_vecino(
            email="emitido@example.com",
        )

        solicitud = self.crear_solicitud(
            vecino,
            estado=SolicitudCertificado.Estado.APROBADA,
        )

        directiva = self.crear_directiva()

        self.login(
            directiva
        )

        response = self.client.post(
            reverse(
                "certificados:emitir",
                args=[solicitud.pk],
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "certificados:gestion"
            ),
        )

        solicitud.refresh_from_db()

        self.assertEqual(
            solicitud.estado,
            SolicitudCertificado.Estado.EMITIDA,
        )

        certificado = Certificado.objects.get(
            solicitud=solicitud
        )

        self.assertEqual(
            len(mail.outbox),
            1,
        )

        correo = mail.outbox[0]

        self.assertEqual(
            correo.to,
            ["emitido@example.com"],
        )

        self.assertIn(
            "certificado",
            correo.subject.lower(),
        )

        self.assertEqual(
            len(correo.attachments),
            1,
        )

        adjunto = correo.attachments[0]

        self.assertEqual(
            adjunto.filename,
            nombre_archivo_certificado(
                certificado
            ),
        )

        self.assertEqual(
            adjunto.mimetype,
            "application/pdf",
        )

        self.assertTrue(
            adjunto.content.startswith(
                b"%PDF-"
            )
        )


    # ========================================================
    # TOLERANCIA A FALLOS SMTP
    # ========================================================

    @patch(
        "certificados.views.enviar_resolucion_certificado",
        side_effect=Exception("SMTP no disponible"),
    )
    def test_fallo_email_no_revierte_resolucion(
        self,
        enviar_mock,
    ):

        _, vecino = self.crear_vecino()

        solicitud = self.crear_solicitud(
            vecino
        )

        directiva = self.crear_directiva()

        self.login(
            directiva
        )

        response = self.client.post(
            reverse(
                "certificados:resolver",
                args=[
                    solicitud.pk,
                    "aprobar",
                ],
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "certificados:pendientes"
            ),
        )

        solicitud.refresh_from_db()

        self.assertEqual(
            solicitud.estado,
            SolicitudCertificado.Estado.APROBADA,
        )

        enviar_mock.assert_called_once()


    @patch(
        "certificados.views.enviar_certificado_emitido",
        side_effect=Exception("SMTP no disponible"),
    )
    def test_fallo_email_no_revierte_emision(
        self,
        enviar_mock,
    ):

        _, vecino = self.crear_vecino()

        solicitud = self.crear_solicitud(
            vecino,
            estado=SolicitudCertificado.Estado.APROBADA,
        )

        directiva = self.crear_directiva()

        self.login(
            directiva
        )

        response = self.client.post(
            reverse(
                "certificados:emitir",
                args=[solicitud.pk],
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "certificados:gestion"
            ),
        )

        solicitud.refresh_from_db()

        self.assertEqual(
            solicitud.estado,
            SolicitudCertificado.Estado.EMITIDA,
        )

        self.assertTrue(
            Certificado.objects.filter(
                solicitud=solicitud
            ).exists()
        )

        enviar_mock.assert_called_once()