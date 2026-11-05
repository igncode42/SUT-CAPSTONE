from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from usuarios.models import Rol
from vecinos.models import Vecino

from .models import Certificado, SolicitudCertificado


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


    def crear_directiva(self):

        rol = Rol.objects.create(
            nombre="Directiva"
        )

        return Usuario.objects.create_user(
            username="directiva",
            password="ClaveSegura123!",
            rol=rol,
        )


    def crear_certificado(self, solicitud):

        vecino = solicitud.vecino

        return Certificado.objects.create(
            solicitud=solicitud,
            nombre_vecino=vecino.nombre,
            apellido_vecino=vecino.apellido,
            identificacion_vecino=vecino.identificacion,
            direccion_vecino=vecino.direccion,
        )


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

        solicitud_a = SolicitudCertificado.objects.create(
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
            f"Solicitud #{solicitud_a.pk}",
        )

        self.assertNotContains(
            response,
            f"Solicitud #{solicitud_b.pk}",
        )


    def test_no_crea_otra_solicitud_si_existe_una_activa(self):

        usuario, vecino = self.crear_vecino(
            "vecino_solicitud_activa"
        )

        SolicitudCertificado.objects.create(
            vecino=vecino,
            estado=SolicitudCertificado.Estado.PENDIENTE,
        )

        self.login(usuario.username)

        response = self.client.post(
            reverse("certificados:solicitar"),
            follow=True,
        )

        self.assertEqual(
            SolicitudCertificado.objects.filter(
                vecino=vecino
            ).count(),
            1,
        )

        self.assertContains(
            response,
            "Ya tienes una solicitud de certificado en proceso.",
        )


    def test_puede_solicitar_nuevamente_si_anterior_esta_emitida(self):

        usuario, vecino = self.crear_vecino(
            "vecino_certificado_emitido"
        )

        SolicitudCertificado.objects.create(
            vecino=vecino,
            estado=SolicitudCertificado.Estado.EMITIDA,
        )

        self.login(usuario.username)

        response = self.client.post(
            reverse("certificados:solicitar")
        )

        self.assertRedirects(
            response,
            reverse("certificados:mis_solicitudes"),
        )

        solicitudes = SolicitudCertificado.objects.filter(
            vecino=vecino
        )

        self.assertEqual(
            solicitudes.count(),
            2,
        )

        self.assertTrue(
            solicitudes.filter(
                estado=SolicitudCertificado.Estado.PENDIENTE,
            ).exists()
        )


    def test_bd_rechaza_estado_invalido(self):

        _, vecino = self.crear_vecino(
            "vecino_estado_invalido"
        )

        with self.assertRaises(IntegrityError):

            with transaction.atomic():

                SolicitudCertificado.objects.create(
                    vecino=vecino,
                    estado="ESTADO_INVENTADO",
                )


    def test_vecino_no_puede_ver_certificado_de_otro(self):

        usuario_a, vecino_a = self.crear_vecino(
            "vecino_certificado_a"
        )

        usuario_b, vecino_b = self.crear_vecino(
            "vecino_certificado_b"
        )

        solicitud_b = SolicitudCertificado.objects.create(
            vecino=vecino_b,
            estado=SolicitudCertificado.Estado.EMITIDA,
        )

        self.crear_certificado(
            solicitud_b
        )

        self.login(usuario_a.username)

        response = self.client.get(
            reverse(
                "certificados:ver",
                args=[solicitud_b.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )


    def test_vecino_puede_ver_su_certificado_emitido(self):

        usuario, vecino = self.crear_vecino(
            "vecino_certificado_propio"
        )

        solicitud = SolicitudCertificado.objects.create(
            vecino=vecino,
            estado=SolicitudCertificado.Estado.EMITIDA,
        )

        certificado = self.crear_certificado(
            solicitud
        )

        self.login(usuario.username)

        response = self.client.get(
            reverse(
                "certificados:ver",
                args=[solicitud.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "certificados/ver_certificado.html",
        )

        self.assertContains(
            response,
            certificado.nombre_vecino,
        )

        self.assertContains(
            response,
            certificado.identificacion_vecino,
        )


    def test_no_puede_ver_certificado_si_solicitud_no_esta_emitida(self):

        usuario, vecino = self.crear_vecino(
            "vecino_pendiente"
        )

        solicitud = SolicitudCertificado.objects.create(
            vecino=vecino,
            estado=SolicitudCertificado.Estado.PENDIENTE,
        )

        self.login(usuario.username)

        response = self.client.get(
            reverse(
                "certificados:ver",
                args=[solicitud.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )


    def test_certificado_conserva_datos_historicos_tras_cambio_vecino(self):

        usuario, vecino = self.crear_vecino(
            "vecino_snapshot"
        )

        solicitud = SolicitudCertificado.objects.create(
            vecino=vecino,
            estado=SolicitudCertificado.Estado.APROBADA,
        )

        directiva = self.crear_directiva()

        self.login(
            directiva.username
        )

        response = self.client.post(
            reverse(
                "certificados:emitir",
                args=[solicitud.pk],
            )
        )

        self.assertRedirects(
            response,
            reverse("certificados:gestion"),
        )

        certificado = Certificado.objects.get(
            solicitud=solicitud
        )

        self.assertEqual(
            certificado.nombre_vecino,
            "Nombre",
        )

        self.assertEqual(
            certificado.apellido_vecino,
            "Prueba",
        )

        self.assertEqual(
            certificado.identificacion_vecino,
            "ID-vecino_snapshot",
        )

        self.assertEqual(
            certificado.direccion_vecino,
            "Dirección de prueba",
        )

        vecino.nombre = "Nombre actualizado"
        vecino.apellido = "Apellido actualizado"
        vecino.identificacion = "ID-ACTUALIZADO"
        vecino.direccion = "Dirección actualizada"

        vecino.save(
            update_fields=[
                "nombre",
                "apellido",
                "identificacion",
                "direccion",
            ]
        )

        certificado.refresh_from_db()

        self.assertEqual(
            certificado.nombre_vecino,
            "Nombre",
        )

        self.assertEqual(
            certificado.apellido_vecino,
            "Prueba",
        )

        self.assertEqual(
            certificado.identificacion_vecino,
            "ID-vecino_snapshot",
        )

        self.assertEqual(
            certificado.direccion_vecino,
            "Dirección de prueba",
        )