from django.test import TestCase
from django.urls import reverse


class SeguridadBasicaTests(TestCase):

    def test_admin_requiere_autenticacion(self):
        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_home_es_publica(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)