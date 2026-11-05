import html

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from usuarios.models import Rol
from vecinos.models import Vecino

from .models import Aviso, Noticia


Usuario = get_user_model()


class ComunicacionesTests(TestCase):

    def setUp(self):

        self.usuario = Usuario.objects.create_user(
            username="autor_comunicaciones",
            password="SUT-Comunicaciones-2026!",
        )

        self.rol_directiva = Rol.objects.create(
            nombre="Directiva",
        )

        self.directiva = Usuario.objects.create_user(
            username="directiva_comunicaciones",
            password="SUT-Directiva-2026!",
            rol=self.rol_directiva,
        )

        self.usuario_vecino = Usuario.objects.create_user(
            username="vecino_comunicaciones",
            password="SUT-Vecino-2026!",
        )

        self.vecino = Vecino.objects.create(
            usuario=self.usuario_vecino,
            nombre="Vecino",
            apellido="Comunicaciones",
            identificacion="SUT-COM-001",
            direccion="Calle Comunicaciones 123",
        )

        Noticia.objects.create(
            usuario=self.usuario,
            titulo="Noticia de prueba",
            contenido="Contenido de noticia de prueba.",
        )

        Aviso.objects.create(
            usuario=self.usuario,
            titulo="Aviso de prueba",
            contenido="Contenido de aviso de prueba.",
        )


    def test_comunicaciones_responde_200(self):

        response = self.client.get(
            reverse("comunicaciones:inicio")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "comunicaciones/inicio.html",
        )


    def test_muestra_noticia_y_aviso_publicados(self):

        response = self.client.get(
            reverse("comunicaciones:inicio")
        )

        self.assertContains(
            response,
            "Noticia de prueba",
        )

        self.assertContains(
            response,
            "Contenido de noticia de prueba.",
        )

        self.assertContains(
            response,
            "Aviso de prueba",
        )

        self.assertContains(
            response,
            "Contenido de aviso de prueba.",
        )


    def test_noticias_se_ordenan_mas_recientes_primero(self):

        noticia_antigua = Noticia.objects.get(
            titulo="Noticia de prueba"
        )

        noticia_nueva = Noticia.objects.create(
            usuario=self.usuario,
            titulo="Noticia más reciente",
            contenido="Contenido reciente.",
        )

        response = self.client.get(
            reverse("comunicaciones:inicio")
        )

        noticias = list(
            response.context["noticias"]
        )

        self.assertEqual(
            noticias[0],
            noticia_nueva,
        )

        self.assertEqual(
            noticias[1],
            noticia_antigua,
        )


    def test_directiva_puede_publicar_noticia(self):

        self.client.login(
            username="directiva_comunicaciones",
            password="SUT-Directiva-2026!",
        )

        response = self.client.post(
            reverse("comunicaciones:publicar_noticia"),
            {
                "titulo": "Nueva noticia comunitaria",
                "contenido": "Información para la comunidad.",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        noticia = Noticia.objects.get(
            titulo="Nueva noticia comunitaria"
        )

        self.assertEqual(
            noticia.usuario,
            self.directiva,
        )

        self.assertEqual(
            noticia.contenido,
            "Información para la comunidad.",
        )


    def test_directiva_puede_publicar_aviso(self):

        self.client.login(
            username="directiva_comunicaciones",
            password="SUT-Directiva-2026!",
        )

        response = self.client.post(
            reverse("comunicaciones:publicar_aviso"),
            {
                "titulo": "Nuevo aviso comunitario",
                "contenido": "Aviso importante para los vecinos.",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        aviso = Aviso.objects.get(
            titulo="Nuevo aviso comunitario"
        )

        self.assertEqual(
            aviso.usuario,
            self.directiva,
        )

        self.assertEqual(
            aviso.contenido,
            "Aviso importante para los vecinos.",
        )


    def test_vecino_no_puede_publicar_noticia(self):

        self.client.login(
            username="vecino_comunicaciones",
            password="SUT-Vecino-2026!",
        )

        response = self.client.post(
            reverse("comunicaciones:publicar_noticia"),
            {
                "titulo": "Noticia no autorizada",
                "contenido": "Este contenido no debe publicarse.",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertFalse(
            Noticia.objects.filter(
                titulo="Noticia no autorizada"
            ).exists()
        )


    def test_vecino_no_puede_publicar_aviso(self):

        self.client.login(
            username="vecino_comunicaciones",
            password="SUT-Vecino-2026!",
        )

        response = self.client.post(
            reverse("comunicaciones:publicar_aviso"),
            {
                "titulo": "Aviso no autorizado",
                "contenido": "Este aviso no debe publicarse.",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertFalse(
            Aviso.objects.filter(
                titulo="Aviso no autorizado"
            ).exists()
        )


    def test_usuario_no_autenticado_es_redirigido_al_login(self):

        response = self.client.get(
            reverse("comunicaciones:publicar_noticia")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertIn(
            reverse("login"),
            response.url,
        )


    def test_contenido_html_se_muestra_escapado(self):

        contenido_peligroso = (
            "<script>alert('SUT-XSS')</script>"
        )

        Noticia.objects.create(
            usuario=self.directiva,
            titulo="Prueba XSS",
            contenido=contenido_peligroso,
        )

        response = self.client.get(
            reverse("comunicaciones:inicio")
        )

        contenido_respuesta = (
            response.content.decode()
        )

        self.assertNotIn(
            contenido_peligroso,
            contenido_respuesta,
        )

        self.assertIn(
            html.escape(contenido_peligroso),
            contenido_respuesta,
        )