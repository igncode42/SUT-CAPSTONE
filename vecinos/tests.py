from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from usuarios.models import Rol

from .models import Vecino


Usuario = get_user_model()


class RegistroVecinoTests(TestCase):

    def setUp(self):
        self.url = reverse("vecinos:registro")


    def test_pagina_registro_responde_200(self):

        response = self.client.get(
            self.url
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "vecinos/registro.html",
        )


    def test_registro_valido_crea_usuario_y_vecino(self):

        datos = {
            "username": "vecino_test",
            "email": "vecino@example.com",
            "nombre": "Vecino",
            "apellido": "Prueba",
            "identificacion": "SUT-TEST-002",
            "direccion": "Calle Prueba 123",
            "password1": "SUT-Prueba-2026!",
            "password2": "SUT-Prueba-2026!",
        }

        response = self.client.post(
            self.url,
            datos,
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        usuario = Usuario.objects.get(
            username="vecino_test"
        )

        vecino = Vecino.objects.get(
            usuario=usuario
        )

        self.assertEqual(
            usuario.email,
            "vecino@example.com",
        )

        self.assertEqual(
            vecino.nombre,
            "Vecino",
        )

        self.assertEqual(
            vecino.apellido,
            "Prueba",
        )

        self.assertEqual(
            vecino.identificacion,
            "SUT-TEST-002",
        )

        self.assertEqual(
            vecino.direccion,
            "Calle Prueba 123",
        )


    def test_registro_publico_no_otorga_privilegios(self):

        datos = {
            "username": "vecino_sin_privilegios",
            "email": "sinprivilegios@example.com",
            "nombre": "Vecino",
            "apellido": "Seguro",
            "identificacion": "SUT-TEST-003",
            "direccion": "Avenida Seguridad 456",
            "password1": "SUT-Seguro-2026!",
            "password2": "SUT-Seguro-2026!",
        }

        self.client.post(
            self.url,
            datos,
        )

        usuario = Usuario.objects.get(
            username="vecino_sin_privilegios"
        )

        vecino = Vecino.objects.get(
            usuario=usuario
        )

        self.assertIsNone(
            usuario.rol
        )

        self.assertFalse(
            usuario.is_staff
        )

        self.assertFalse(
            usuario.is_superuser
        )

        self.assertFalse(
            vecino.miembro_junta
        )


    def test_identificacion_duplicada_es_rechazada(self):

        usuario_existente = Usuario.objects.create_user(
            username="vecino_existente",
            password="SUT-Existente-2026!",
        )

        Vecino.objects.create(
            usuario=usuario_existente,
            nombre="Vecino",
            apellido="Existente",
            identificacion="SUT-DUPLICADA-001",
            direccion="Calle Existente 123",
        )

        datos = {
            "username": "vecino_nuevo",
            "email": "nuevo@example.com",
            "nombre": "Vecino",
            "apellido": "Nuevo",
            "identificacion": "SUT-DUPLICADA-001",
            "direccion": "Calle Nueva 456",
            "password1": "SUT-Nuevo-2026!",
            "password2": "SUT-Nuevo-2026!",
        }

        response = self.client.post(
            self.url,
            datos,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertFalse(
            Usuario.objects
            .filter(
                username="vecino_nuevo"
            )
            .exists()
        )

        self.assertEqual(
            Vecino.objects
            .filter(
                identificacion="SUT-DUPLICADA-001"
            )
            .count(),
            1,
        )

        self.assertContains(
            response,
            "Ya existe un vecino registrado con esta identificación.",
        )


class GestionVecinoTests(TestCase):

    def setUp(self):

        self.rol_directiva = Rol.objects.create(
            nombre="Directiva"
        )

        self.rol_autorizado = Rol.objects.create(
            nombre="Personal autorizado"
        )

        self.directiva = Usuario.objects.create_user(
            username="directiva_vecinos",
            password="SUT-Directiva-2026!",
            rol=self.rol_directiva,
        )

        self.autorizado = Usuario.objects.create_user(
            username="autorizado_vecinos",
            password="SUT-Autorizado-2026!",
            rol=self.rol_autorizado,
        )

        self.usuario_vecino = Usuario.objects.create_user(
            username="vecino_gestion",
            password="SUT-Vecino-2026!",
        )

        self.vecino = Vecino.objects.create(
            usuario=self.usuario_vecino,
            nombre="Vecino",
            apellido="Gestionado",
            identificacion="SUT-GESTION-001",
            direccion="Calle Gestión 123",
        )

        self.usuario_miembro = Usuario.objects.create_user(
            username="miembro_gestion",
            password="SUT-Miembro-2026!",
        )

        self.miembro = Vecino.objects.create(
            usuario=self.usuario_miembro,
            nombre="Miembro",
            apellido="Junta",
            identificacion="SUT-GESTION-002",
            direccion="Calle Junta 456",
            miembro_junta=True,
        )

        self.url_gestion = reverse(
            "vecinos:gestion"
        )


    def test_directiva_puede_ver_gestion_vecinos(self):

        self.client.login(
            username="directiva_vecinos",
            password="SUT-Directiva-2026!",
        )

        response = self.client.get(
            self.url_gestion
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "vecinos/gestion.html",
        )

        self.assertContains(
            response,
            "Vecino Gestionado",
        )


    def test_personal_autorizado_puede_ver_gestion_vecinos(self):

        self.client.login(
            username="autorizado_vecinos",
            password="SUT-Autorizado-2026!",
        )

        response = self.client.get(
            self.url_gestion
        )

        self.assertEqual(
            response.status_code,
            200,
        )


    def test_vecino_normal_no_puede_ver_gestion(self):

        self.client.login(
            username="vecino_gestion",
            password="SUT-Vecino-2026!",
        )

        response = self.client.get(
            self.url_gestion
        )

        self.assertEqual(
            response.status_code,
            403,
        )


    def test_miembro_junta_no_puede_ver_gestion(self):

        self.client.login(
            username="miembro_gestion",
            password="SUT-Miembro-2026!",
        )

        response = self.client.get(
            self.url_gestion
        )

        self.assertEqual(
            response.status_code,
            403,
        )


    def test_anonimo_es_redirigido_al_login(self):

        response = self.client.get(
            self.url_gestion
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url_gestion}",
        )


    def test_directiva_puede_convertir_vecino_en_miembro(self):

        self.client.login(
            username="directiva_vecinos",
            password="SUT-Directiva-2026!",
        )

        response = self.client.post(
            reverse(
                "vecinos:actualizar_miembro",
                args=[self.vecino.id],
            ),
            {
                "miembro_junta": "true",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.vecino.refresh_from_db()

        self.assertTrue(
            self.vecino.miembro_junta
        )


    def test_directiva_puede_quitar_condicion_de_miembro(self):

        self.client.login(
            username="directiva_vecinos",
            password="SUT-Directiva-2026!",
        )

        response = self.client.post(
            reverse(
                "vecinos:actualizar_miembro",
                args=[self.miembro.id],
            ),
            {
                "miembro_junta": "false",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.miembro.refresh_from_db()

        self.assertFalse(
            self.miembro.miembro_junta
        )


    def test_vecino_normal_no_puede_convertirse_en_miembro(self):

        self.client.login(
            username="vecino_gestion",
            password="SUT-Vecino-2026!",
        )

        response = self.client.post(
            reverse(
                "vecinos:actualizar_miembro",
                args=[self.vecino.id],
            ),
            {
                "miembro_junta": "true",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.vecino.refresh_from_db()

        self.assertFalse(
            self.vecino.miembro_junta
        )


    def test_anonimo_no_puede_modificar_membresia(self):

        response = self.client.post(
            reverse(
                "vecinos:actualizar_miembro",
                args=[self.vecino.id],
            ),
            {
                "miembro_junta": "true",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.vecino.refresh_from_db()

        self.assertFalse(
            self.vecino.miembro_junta
        )