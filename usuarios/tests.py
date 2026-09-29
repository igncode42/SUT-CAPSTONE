from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


Usuario = get_user_model()


class SeguridadBasicaTests(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="vecino_test",
            password="ClaveSegura123!"
        )

    def test_home_es_publica(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

    def test_admin_requiere_autenticacion(self):
        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_login_carga_correctamente(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_panel_requiere_autenticacion(self):
        response = self.client.get(reverse("panel"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_usuario_autenticado_puede_ver_panel(self):
        self.client.login(
            username="vecino_test",
            password="ClaveSegura123!"
        )

        response = self.client.get(reverse("panel"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "usuarios/panel.html")

    def test_login_correcto_redirige_al_panel(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "vecino_test",
                "password": "ClaveSegura123!",
            },
        )

        self.assertRedirects(response, reverse("panel"))

    def test_logout_cierra_sesion(self):
        self.client.login(
            username="vecino_test",
            password="ClaveSegura123!"
        )

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("home"))

        response_panel = self.client.get(reverse("panel"))

        self.assertEqual(response_panel.status_code, 302)
        self.assertIn(reverse("login"), response_panel.url)
