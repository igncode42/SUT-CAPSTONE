from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from usuarios.models import Rol
from vecinos.models import Vecino

from .models import (
    Certificado,
    SolicitudCertificado,
)


Usuario = get_user_model()


class GestionCertificadoTests(TestCase):

    def crear_usuario(
        self,
        username,
        rol=None,
    ):

        return Usuario.objects.create_user(
            username=username,
            password="ClaveSegura123!",
            rol=rol,
        )


    def crear_vecino(
        self,
        usuario,
    ):

        return Vecino.objects.create(
            usuario=usuario,
            nombre="Nombre",
            apellido="Prueba",
            identificacion=f"ID-{usuario.username}",
            direccion="Dirección de prueba",
        )


    def crear_solicitud(self):

        usuario = self.crear_usuario(
            "solicitante"
        )

        vecino = self.crear_vecino(
            usuario
        )

        return SolicitudCertificado.objects.create(
            vecino=vecino,
        )


    def crear_directiva(self):

        rol = Rol.objects.create(
            nombre="Directiva"
        )

        return self.crear_usuario(
            "directiva",
            rol=rol,
        )


    def login(self, usuario):

        return self.client.login(
            username=usuario.username,
            password="ClaveSegura123!",
        )


    def test_anonimo_no_puede_ver_pendientes(self):

        response = self.client.get(
            reverse(
                "certificados:pendientes"
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )


    def test_vecino_no_puede_gestionar(self):

        usuario = self.crear_usuario(
            "vecino"
        )

        self.crear_vecino(
            usuario
        )

        self.login(usuario)

        response = self.client.get(
            reverse(
                "certificados:gestion"
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )


    def test_directiva_puede_ver_pendientes(self):

        solicitud = self.crear_solicitud()

        directiva = self.crear_directiva()

        self.login(directiva)

        response = self.client.get(
            reverse(
                "certificados:pendientes"
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            f"Solicitud #{solicitud.pk}",
        )


    def test_directiva_puede_aprobar(self):

        solicitud = self.crear_solicitud()

        directiva = self.crear_directiva()

        self.login(directiva)

        self.client.post(
            reverse(
                "certificados:resolver",
                args=[
                    solicitud.pk,
                    "aprobar",
                ],
            )
        )

        solicitud.refresh_from_db()

        self.assertEqual(
            solicitud.estado,
            SolicitudCertificado.Estado.APROBADA,
        )


    def test_directiva_puede_rechazar(self):

        solicitud = self.crear_solicitud()

        directiva = self.crear_directiva()

        self.login(directiva)

        self.client.post(
            reverse(
                "certificados:resolver",
                args=[
                    solicitud.pk,
                    "rechazar",
                ],
            )
        )

        solicitud.refresh_from_db()

        self.assertEqual(
            solicitud.estado,
            SolicitudCertificado.Estado.RECHAZADA,
        )


    def test_solicitud_rechazada_no_puede_emitirse(self):

        solicitud = self.crear_solicitud()

        solicitud.estado = (
            SolicitudCertificado.Estado.RECHAZADA
        )

        solicitud.save()

        directiva = self.crear_directiva()

        self.login(directiva)

        response = self.client.post(
            reverse(
                "certificados:emitir",
                args=[solicitud.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertEqual(
            Certificado.objects.count(),
            0,
        )


    def test_solicitud_aprobada_puede_emitirse(self):

        solicitud = self.crear_solicitud()

        solicitud.estado = (
            SolicitudCertificado.Estado.APROBADA
        )

        solicitud.save()

        directiva = self.crear_directiva()

        self.login(directiva)

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


    def test_certificado_no_puede_emitirse_dos_veces(self):

        solicitud = self.crear_solicitud()

        solicitud.estado = (
            SolicitudCertificado.Estado.APROBADA
        )

        solicitud.save()

        directiva = self.crear_directiva()

        self.login(directiva)

        self.client.post(
            reverse(
                "certificados:emitir",
                args=[solicitud.pk],
            )
        )

        response = self.client.post(
            reverse(
                "certificados:emitir",
                args=[solicitud.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertEqual(
            Certificado.objects.count(),
            1,
        )
