from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from vecinos.models import Vecino

from .models import ProyectoVecinal


Usuario = get_user_model()


class ProyectoVecinalTests(TestCase):

    def crear_usuario_vecino(
        self,
        username,
        miembro_junta,
    ):

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
            miembro_junta=miembro_junta,
        )

        return usuario, vecino


    def login(self, username):
        return self.client.login(
            username=username,
            password="ClaveSegura123!",
        )


    def test_anonimo_no_puede_postular(self):

        response = self.client.get(
            reverse("proyectos:crear")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertIn(
            reverse("login"),
            response.url,
        )


    def test_vecino_comun_no_puede_postular(self):

        self.crear_usuario_vecino(
            "vecino_comun",
            False,
        )

        self.login("vecino_comun")

        response = self.client.get(
            reverse("proyectos:crear")
        )

        self.assertEqual(
            response.status_code,
            403,
        )


    def test_miembro_junta_puede_ver_formulario(self):

        self.crear_usuario_vecino(
            "miembro",
            True,
        )

        self.login("miembro")

        response = self.client.get(
            reverse("proyectos:crear")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "proyectos/crear.html",
        )


    def test_postulacion_crea_proyecto_pendiente(self):

        usuario, vecino = self.crear_usuario_vecino(
            "miembro",
            True,
        )

        self.login(usuario.username)

        response = self.client.post(
            reverse("proyectos:crear"),
            {
                "titulo": "Mejoramiento plaza",
                "descripcion": "Proyecto comunitario de prueba.",
            },
        )

        self.assertRedirects(
            response,
            reverse("proyectos:mis_proyectos"),
        )

        proyecto = ProyectoVecinal.objects.get()

        self.assertEqual(
            proyecto.vecino,
            vecino,
        )

        self.assertEqual(
            proyecto.estado,
            ProyectoVecinal.Estado.PENDIENTE,
        )


    def test_usuario_no_puede_forzar_estado_aprobado(self):

        usuario, vecino = self.crear_usuario_vecino(
            "miembro",
            True,
        )

        self.login(usuario.username)

        self.client.post(
            reverse("proyectos:crear"),
            {
                "titulo": "Proyecto seguro",
                "descripcion": "Intento de cambiar el estado.",
                "estado": ProyectoVecinal.Estado.APROBADO,
            },
        )

        proyecto = ProyectoVecinal.objects.get(
            vecino=vecino
        )

        self.assertEqual(
            proyecto.estado,
            ProyectoVecinal.Estado.PENDIENTE,
        )


    def test_mis_proyectos_solo_muestra_propios(self):

        usuario_a, vecino_a = self.crear_usuario_vecino(
            "miembro_a",
            True,
        )

        usuario_b, vecino_b = self.crear_usuario_vecino(
            "miembro_b",
            True,
        )

        ProyectoVecinal.objects.create(
            vecino=vecino_a,
            titulo="Proyecto A",
            descripcion="Pertenece al usuario A",
        )

        ProyectoVecinal.objects.create(
            vecino=vecino_b,
            titulo="Proyecto B",
            descripcion="Pertenece al usuario B",
        )

        self.login(usuario_a.username)

        response = self.client.get(
            reverse("proyectos:mis_proyectos")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Proyecto A",
        )

        self.assertNotContains(
            response,
            "Proyecto B",
        )
