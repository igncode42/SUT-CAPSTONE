from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from vecinos.models import Vecino

from .models import SolicitudCertificado


Usuario = get_user_model()


class SolicitudCertificadoTests(TestCase):

    def crear_vecino(self, username):

        usuario = Usuario.objects.create_user(
            username=username,
            password="ClaveSegura123!",
        )

        vecino = Vecino.objects.create(
            usuario=usuario,
            nombre="Nombre",
            apellido="Prueba",
            identificacion=f"ID-{username}",
            direccion="Dirección de prueba",
        )

        return usuario, vecino


    def login(self, username):

        return self.client.login(
            username=username,
            password="ClaveSegura123!",
        )


    def test_anonimo_no_puede_ver_solicitudes(self):

        response = self.client.get(
            reverse(
                "certificados:mis_solicitudes"
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )


    def test_usuario_sin_vecino_no_puede_solicitar(self):

        usuario = Usuario.objects.create_user(
            username="sin_vecino",
            password="ClaveSegura123!",
        )

        self.login(usuario.username)

        response = self.client.post(
            reverse("certificados:solicitar")
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertEqual(
            SolicitudCertificado.objects.count(),
            0,
        )


    def test_vecino_puede_solicitar_certificado(self):

        usuario, vecino = self.crear_vecino(
            "vecino"
        )

        self.login(usuario.username)

        response = self.client.post(
            reverse("certificados:solicitar")
        )

        self.assertRedirects(
            response,
            reverse(
                "certificados:mis_solicitudes"
            ),
        )

        solicitud = SolicitudCertificado.objects.get()

        self.assertEqual(
            solicitud.vecino,
            vecino,
        )

        self.assertEqual(
            solicitud.estado,
            SolicitudCertificado.Estado.PENDIENTE,
        )


    def test_get_no_crea_solicitud(self):

        usuario, vecino = self.crear_vecino(
            "vecino"
        )

        self.login(usuario.username)

        response = self.client.get(
            reverse("certificados:solicitar")
        )

        self.assertEqual(
            response.status_code,
            405,
        )

        self.assertEqual(
            SolicitudCertificado.objects.count(),
            0,
        )


    def test_solo_muestra_solicitudes_propias(self):

        usuario_a, vecino_a = self.crear_vecino(
            "vecino_a"
        )

        usuario_b, vecino_b = self.crear_vecino(
            "vecino_b"
        )

        SolicitudCertificado.objects.create(
            vecino=vecino_a,
        )

        solicitud_b = SolicitudCertificado.objects.create(
            vecino=vecino_b,
        )

        self.login(usuario_a.username)

        response = self.client.get(
            reverse(
                "certificados:mis_solicitudes"
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Solicitud #1",
        )

        self.assertNotContains(
            response,
            f"Solicitud #{solicitud_b.pk}",
        )
