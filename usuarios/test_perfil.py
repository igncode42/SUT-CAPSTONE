from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from vecinos.models import Vecino


Usuario = get_user_model()


class PerfilUsuarioTests(TestCase):

    def setUp(self):

        self.password = "ClaveSegura123!"

        self.usuario = Usuario.objects.create_user(
            username="vecino_perfil",
            password=self.password,
            email="original@example.com",
        )

        self.vecino = Vecino.objects.create(
            usuario=self.usuario,
            nombre="Nombre",
            apellido="Original",
            identificacion="PERFIL-001",
            direccion="Dirección original",
        )

        self.url = reverse(
            "perfil"
        )


    def login(self):

        return self.client.login(
            username=self.usuario.username,
            password=self.password,
        )


    def test_vecino_puede_ver_su_perfil(self):

        self.login()

        response = self.client.get(
            self.url
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Mi perfil",
        )

        self.assertContains(
            response,
            self.usuario.username,
        )

        self.assertContains(
            response,
            self.vecino.identificacion,
        )


    def test_vecino_puede_actualizar_datos_editables(self):

        self.login()

        response = self.client.post(
            self.url,
            {
                "email": "nuevo@example.com",
                "nombre": "Nombre Nuevo",
                "apellido": "Apellido Nuevo",
                "direccion": "Nueva dirección 123",
            },
        )

        self.assertRedirects(
            response,
            self.url,
        )

        self.usuario.refresh_from_db()
        self.vecino.refresh_from_db()

        self.assertEqual(
            self.usuario.email,
            "nuevo@example.com",
        )

        self.assertEqual(
            self.vecino.nombre,
            "Nombre Nuevo",
        )

        self.assertEqual(
            self.vecino.apellido,
            "Apellido Nuevo",
        )

        self.assertEqual(
            self.vecino.direccion,
            "Nueva dirección 123",
        )


    def test_identificacion_no_se_modifica_desde_perfil(self):

        self.login()

        identificacion_original = (
            self.vecino.identificacion
        )

        response = self.client.post(
            self.url,
            {
                "email": "nuevo@example.com",
                "nombre": "Nombre",
                "apellido": "Original",
                "direccion": "Dirección modificada",
                "identificacion": "INTENTO-CAMBIO",
            },
        )

        self.assertRedirects(
            response,
            self.url,
        )

        self.vecino.refresh_from_db()

        self.assertEqual(
            self.vecino.identificacion,
            identificacion_original,
        )


    def test_perfil_muestra_datos_del_usuario_autenticado(self):

        otro_usuario = Usuario.objects.create_user(
            username="otro_vecino",
            password=self.password,
            email="otro@example.com",
        )

        otro_vecino = Vecino.objects.create(
            usuario=otro_usuario,
            nombre="Otro",
            apellido="Vecino",
            identificacion="PERFIL-002",
            direccion="Otra dirección",
        )

        self.login()

        response = self.client.get(
            self.url
        )

        self.assertContains(
            response,
            self.vecino.identificacion,
        )

        self.assertNotContains(
            response,
            otro_vecino.identificacion,
        )