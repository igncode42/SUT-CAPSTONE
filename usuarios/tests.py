from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Rol
from .permisos import (
    puede_gestionar_certificados,
    puede_gestionar_vecinos,
    puede_publicar_comunicaciones,
    puede_resolver_proyectos,
)


Usuario = get_user_model()


PERMISOS_ADMINISTRATIVOS = (
    puede_resolver_proyectos,
    puede_gestionar_certificados,
    puede_publicar_comunicaciones,
    puede_gestionar_vecinos,
)


class SeguridadBasicaTests(TestCase):

    def setUp(self):

        self.usuario = Usuario.objects.create_user(
            username="vecino_test",
            password="ClaveSegura123!",
        )


    def test_home_es_publica(self):

        response = self.client.get(
            reverse("home")
        )

        self.assertEqual(
            response.status_code,
            200,
        )


    def test_admin_requiere_autenticacion(self):

        response = self.client.get(
            "/admin/"
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertIn(
            "/admin/login/",
            response.url,
        )


    def test_login_carga_correctamente(self):

        response = self.client.get(
            reverse("login")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "registration/login.html",
        )


    def test_panel_requiere_autenticacion(self):

        response = self.client.get(
            reverse("panel")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertIn(
            reverse("login"),
            response.url,
        )


    def test_usuario_autenticado_puede_ver_panel(self):

        self.client.login(
            username="vecino_test",
            password="ClaveSegura123!",
        )

        response = self.client.get(
            reverse("panel")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "usuarios/panel.html",
        )


    def test_login_correcto_redirige_al_panel(self):

        response = self.client.post(
            reverse("login"),
            {
                "username": "vecino_test",
                "password": "ClaveSegura123!",
            },
        )

        self.assertRedirects(
            response,
            reverse("panel"),
        )


    def test_logout_cierra_sesion(self):

        self.client.login(
            username="vecino_test",
            password="ClaveSegura123!",
        )

        response = self.client.post(
            reverse("logout")
        )

        self.assertRedirects(
            response,
            reverse("home"),
        )

        response_panel = self.client.get(
            reverse("panel")
        )

        self.assertEqual(
            response_panel.status_code,
            302,
        )

        self.assertIn(
            reverse("login"),
            response_panel.url,
        )


class PermisosAdministrativosTests(TestCase):

    def assert_todos_los_permisos(self, usuario, esperado):

        for verificador in PERMISOS_ADMINISTRATIVOS:

            with self.subTest(
                permiso=verificador.__name__
            ):

                self.assertEqual(
                    verificador(usuario),
                    esperado,
                )


    def test_usuario_normal_no_tiene_permisos_administrativos(self):

        usuario = Usuario.objects.create_user(
            username="usuario_normal",
            password="ClaveSegura123!",
        )

        self.assert_todos_los_permisos(
            usuario,
            False,
        )


    def test_staff_sin_rol_no_tiene_permisos_funcionales(self):

        usuario = Usuario.objects.create_user(
            username="staff_tecnico",
            password="ClaveSegura123!",
            is_staff=True,
        )

        self.assertIsNone(
            usuario.rol
        )

        self.assert_todos_los_permisos(
            usuario,
            False,
        )


    def test_directiva_tiene_permisos_administrativos(self):

        rol = Rol.objects.create(
            nombre="Directiva"
        )

        usuario = Usuario.objects.create_user(
            username="directiva",
            password="ClaveSegura123!",
            rol=rol,
        )

        self.assert_todos_los_permisos(
            usuario,
            True,
        )


    def test_personal_autorizado_tiene_permisos_administrativos(self):

        rol = Rol.objects.create(
            nombre="Personal autorizado"
        )

        usuario = Usuario.objects.create_user(
            username="personal_autorizado",
            password="ClaveSegura123!",
            rol=rol,
        )

        self.assert_todos_los_permisos(
            usuario,
            True,
        )


    def test_superuser_tiene_permisos_administrativos(self):

        usuario = Usuario.objects.create_superuser(
            username="superuser",
            password="ClaveSegura123!",
            email="superuser@example.com",
        )

        self.assert_todos_los_permisos(
            usuario,
            True,
        )