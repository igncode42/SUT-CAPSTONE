from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from usuarios.models import Rol
from usuarios.permisos import tiene_rol
from vecinos.models import Vecino


Usuario = get_user_model()


class PermisosBaseTests(TestCase):

    def crear_usuario(self, username):
        return Usuario.objects.create_user(
            username=username,
            password="ClaveSegura123!",
        )

    def crear_vecino(self, usuario, miembro_junta=False):
        return Vecino.objects.create(
            usuario=usuario,
            nombre="Nombre",
            apellido="Prueba",
            identificacion=f"ID-{usuario.username}",
            direccion="Dirección de prueba",
            miembro_junta=miembro_junta,
        )

    def test_anonimo_no_puede_entrar_zona_miembro(self):
        response = self.client.get(
            reverse("panel_miembro")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            reverse("login"),
            response.url,
        )

    def test_vecino_comun_recibe_403(self):
        usuario = self.crear_usuario("vecino_comun")

        self.crear_vecino(
            usuario,
            miembro_junta=False,
        )

        self.client.login(
            username="vecino_comun",
            password="ClaveSegura123!",
        )

        response = self.client.get(
            reverse("panel_miembro")
        )

        self.assertEqual(response.status_code, 403)

    def test_miembro_junta_puede_entrar(self):
        usuario = self.crear_usuario("miembro_junta")

        self.crear_vecino(
            usuario,
            miembro_junta=True,
        )

        self.client.login(
            username="miembro_junta",
            password="ClaveSegura123!",
        )

        response = self.client.get(
            reverse("panel_miembro")
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "usuarios/panel_miembro.html",
        )

    def test_helper_tiene_rol(self):
        rol = Rol.objects.create(
            nombre="Directiva"
        )

        usuario = self.crear_usuario("directiva_test")
        usuario.rol = rol
        usuario.save()

        self.assertTrue(
            tiene_rol(usuario, "directiva")
        )

        self.assertFalse(
            tiene_rol(usuario, "vecino")
        )
