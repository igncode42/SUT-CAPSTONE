from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Vecino


Usuario = get_user_model()


class RegistroVecinoTests(TestCase):
    def setUp(self):
        self.url = reverse("vecinos:registro")

    def test_pagina_registro_responde_200(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "vecinos/registro.html")

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

        response = self.client.post(self.url, datos)

        self.assertEqual(response.status_code, 302)

        usuario = Usuario.objects.get(username="vecino_test")
        vecino = Vecino.objects.get(usuario=usuario)

        self.assertEqual(usuario.email, "vecino@example.com")
        self.assertEqual(vecino.nombre, "Vecino")
        self.assertEqual(vecino.apellido, "Prueba")
        self.assertEqual(vecino.identificacion, "SUT-TEST-002")
        self.assertEqual(vecino.direccion, "Calle Prueba 123")

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

        self.client.post(self.url, datos)

        usuario = Usuario.objects.get(
            username="vecino_sin_privilegios"
        )
        vecino = Vecino.objects.get(usuario=usuario)

        self.assertIsNone(usuario.rol)
        self.assertFalse(usuario.is_staff)
        self.assertFalse(usuario.is_superuser)
        self.assertFalse(vecino.miembro_junta)

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

        response = self.client.post(self.url, datos)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Usuario.objects.filter(username="vecino_nuevo").exists()
        )

        self.assertEqual(
            Vecino.objects.filter(
                identificacion="SUT-DUPLICADA-001"
            ).count(),
            1,
        )

        self.assertContains(
            response,
            "Ya existe un vecino registrado con esta identificación.",
        )