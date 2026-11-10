from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from usuarios.models import Rol
from vecinos.models import Vecino

from .models import Aviso, Noticia


Usuario = get_user_model()


class ComunicacionesCrudTests(TestCase):

    def setUp(self):

        self.password_directiva = "SUT-Directiva-CRUD-2026!"
        self.password_vecino = "SUT-Vecino-CRUD-2026!"

        self.rol_directiva = Rol.objects.create(
            nombre="Directiva",
        )

        self.directiva = Usuario.objects.create_user(
            username="directiva_crud",
            password=self.password_directiva,
            email="directiva@example.com",
            rol=self.rol_directiva,
        )

        self.usuario_vecino = Usuario.objects.create_user(
            username="vecino_crud",
            password=self.password_vecino,
            email="vecino@example.com",
        )

        self.vecino = Vecino.objects.create(
            usuario=self.usuario_vecino,
            nombre="Vecino",
            apellido="CRUD",
            identificacion="CRUD-001",
            direccion="Calle CRUD 123",
        )

        self.noticia = Noticia.objects.create(
            usuario=self.directiva,
            titulo="Noticia original",
            contenido="Contenido original de noticia.",
        )

        self.aviso = Aviso.objects.create(
            usuario=self.directiva,
            titulo="Aviso original",
            contenido="Contenido original de aviso.",
        )


    def login_directiva(self):

        return self.client.login(
            username=self.directiva.username,
            password=self.password_directiva,
        )


    def login_vecino(self):

        return self.client.login(
            username=self.usuario_vecino.username,
            password=self.password_vecino,
        )


    # ========================================================
    # EDITAR NOTICIA
    # ========================================================

    def test_directiva_puede_ver_formulario_editar_noticia(self):

        self.login_directiva()

        response = self.client.get(
            reverse(
                "comunicaciones:editar_noticia",
                args=[self.noticia.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "comunicaciones/editar_noticia.html",
        )

        self.assertContains(
            response,
            "Noticia original",
        )


    def test_directiva_puede_editar_noticia(self):

        self.login_directiva()

        response = self.client.post(
            reverse(
                "comunicaciones:editar_noticia",
                args=[self.noticia.pk],
            ),
            {
                "titulo": "Noticia actualizada",
                "contenido": "Contenido actualizado de noticia.",
            },
        )

        self.assertRedirects(
            response,
            reverse("comunicaciones:inicio"),
        )

        self.noticia.refresh_from_db()

        self.assertEqual(
            self.noticia.titulo,
            "Noticia actualizada",
        )

        self.assertEqual(
            self.noticia.contenido,
            "Contenido actualizado de noticia.",
        )

        self.assertEqual(
            self.noticia.usuario,
            self.directiva,
        )


    # ========================================================
    # ELIMINAR NOTICIA
    # ========================================================

    def test_directiva_puede_ver_confirmacion_eliminar_noticia(self):

        self.login_directiva()

        response = self.client.get(
            reverse(
                "comunicaciones:eliminar_noticia",
                args=[self.noticia.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "comunicaciones/eliminar_noticia.html",
        )

        self.assertContains(
            response,
            "Noticia original",
        )


    def test_directiva_puede_eliminar_noticia(self):

        self.login_directiva()

        pk = self.noticia.pk

        response = self.client.post(
            reverse(
                "comunicaciones:eliminar_noticia",
                args=[pk],
            )
        )

        self.assertRedirects(
            response,
            reverse("comunicaciones:inicio"),
        )

        self.assertFalse(
            Noticia.objects.filter(
                pk=pk,
            ).exists()
        )


    # ========================================================
    # EDITAR AVISO
    # ========================================================

    def test_directiva_puede_ver_formulario_editar_aviso(self):

        self.login_directiva()

        response = self.client.get(
            reverse(
                "comunicaciones:editar_aviso",
                args=[self.aviso.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "comunicaciones/editar_aviso.html",
        )

        self.assertContains(
            response,
            "Aviso original",
        )


    def test_directiva_puede_editar_aviso(self):

        self.login_directiva()

        response = self.client.post(
            reverse(
                "comunicaciones:editar_aviso",
                args=[self.aviso.pk],
            ),
            {
                "titulo": "Aviso actualizado",
                "contenido": "Contenido actualizado de aviso.",
            },
        )

        self.assertRedirects(
            response,
            reverse("comunicaciones:inicio"),
        )

        self.aviso.refresh_from_db()

        self.assertEqual(
            self.aviso.titulo,
            "Aviso actualizado",
        )

        self.assertEqual(
            self.aviso.contenido,
            "Contenido actualizado de aviso.",
        )

        self.assertEqual(
            self.aviso.usuario,
            self.directiva,
        )


    # ========================================================
    # ELIMINAR AVISO
    # ========================================================

    def test_directiva_puede_ver_confirmacion_eliminar_aviso(self):

        self.login_directiva()

        response = self.client.get(
            reverse(
                "comunicaciones:eliminar_aviso",
                args=[self.aviso.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "comunicaciones/eliminar_aviso.html",
        )

        self.assertContains(
            response,
            "Aviso original",
        )


    def test_directiva_puede_eliminar_aviso(self):

        self.login_directiva()

        pk = self.aviso.pk

        response = self.client.post(
            reverse(
                "comunicaciones:eliminar_aviso",
                args=[pk],
            )
        )

        self.assertRedirects(
            response,
            reverse("comunicaciones:inicio"),
        )

        self.assertFalse(
            Aviso.objects.filter(
                pk=pk,
            ).exists()
        )


    # ========================================================
    # SEGURIDAD / PERMISOS
    # ========================================================

    def test_vecino_no_puede_editar_noticia(self):

        self.login_vecino()

        response = self.client.post(
            reverse(
                "comunicaciones:editar_noticia",
                args=[self.noticia.pk],
            ),
            {
                "titulo": "Intento no autorizado",
                "contenido": "No debe persistir.",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.noticia.refresh_from_db()

        self.assertEqual(
            self.noticia.titulo,
            "Noticia original",
        )


    def test_vecino_no_puede_eliminar_noticia(self):

        self.login_vecino()

        pk = self.noticia.pk

        response = self.client.post(
            reverse(
                "comunicaciones:eliminar_noticia",
                args=[pk],
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertTrue(
            Noticia.objects.filter(
                pk=pk,
            ).exists()
        )


    def test_vecino_no_puede_editar_aviso(self):

        self.login_vecino()

        response = self.client.post(
            reverse(
                "comunicaciones:editar_aviso",
                args=[self.aviso.pk],
            ),
            {
                "titulo": "Intento no autorizado",
                "contenido": "No debe persistir.",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.aviso.refresh_from_db()

        self.assertEqual(
            self.aviso.titulo,
            "Aviso original",
        )


    def test_vecino_no_puede_eliminar_aviso(self):

        self.login_vecino()

        pk = self.aviso.pk

        response = self.client.post(
            reverse(
                "comunicaciones:eliminar_aviso",
                args=[pk],
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertTrue(
            Aviso.objects.filter(
                pk=pk,
            ).exists()
        )


    def test_usuario_no_autenticado_no_puede_editar_noticia(self):

        response = self.client.get(
            reverse(
                "comunicaciones:editar_noticia",
                args=[self.noticia.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertIn(
            reverse("login"),
            response.url,
        )


    def test_usuario_no_autenticado_no_puede_eliminar_aviso(self):

        response = self.client.get(
            reverse(
                "comunicaciones:eliminar_aviso",
                args=[self.aviso.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertIn(
            reverse("login"),
            response.url,
        )