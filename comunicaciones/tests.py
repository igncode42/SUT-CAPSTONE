from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Aviso, Noticia


Usuario = get_user_model()


class ComunicacionesTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="autor_comunicaciones",
            password="SUT-Comunicaciones-2026!",
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

        self.assertEqual(response.status_code, 200)

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

        noticias = list(response.context["noticias"])

        self.assertEqual(
            noticias[0],
            noticia_nueva,
        )

        self.assertEqual(
            noticias[1],
            noticia_antigua,
        )