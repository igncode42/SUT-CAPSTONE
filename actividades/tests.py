from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from vecinos.models import Vecino

from .models import Actividad, InscripcionActividad


Usuario = get_user_model()


class ActividadTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="vecino_actividad",
            password="SUT-Actividad-2026!",
        )

        self.vecino = Vecino.objects.create(
            usuario=self.usuario,
            nombre="Vecino",
            apellido="Actividad",
            identificacion="SUT-ACT-001",
            direccion="Calle Actividad 123",
        )

        self.actividad = Actividad.objects.create(
            nombre="Taller Comunitario",
            descripcion="Actividad de prueba.",
            fecha=timezone.now() + timedelta(days=3),
            cupo_maximo=2,
        )

        self.client.login(
            username="vecino_actividad",
            password="SUT-Actividad-2026!",
        )

    def test_actividades_disponibles_responde_200(self):
        response = self.client.get(
            reverse("actividades:disponibles")
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "actividades/disponibles.html",
        )

    def test_inscripcion_valida_crea_registro(self):
        response = self.client.post(
            reverse(
                "actividades:inscribir",
                args=[self.actividad.id],
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.actividad.inscripciones.filter(
                vecino=self.vecino
            ).exists()
        )

    def test_inscripcion_duplicada_no_crea_segundo_registro(self):
        InscripcionActividad.objects.create(
            vecino=self.vecino,
            actividad=self.actividad,
        )

        response = self.client.post(
            reverse(
                "actividades:inscribir",
                args=[self.actividad.id],
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            InscripcionActividad.objects.filter(
                vecino=self.vecino,
                actividad=self.actividad,
            ).count(),
            1,
        )

    def test_actividad_sin_cupos_rechaza_inscripcion(self):
        self.actividad.cupo_maximo = 1
        self.actividad.save()

        otro_usuario = Usuario.objects.create_user(
            username="vecino_ocupa_cupo",
            password="SUT-Otro-2026!",
        )

        otro_vecino = Vecino.objects.create(
            usuario=otro_usuario,
            nombre="Otro",
            apellido="Vecino",
            identificacion="SUT-ACT-002",
            direccion="Calle Otra 456",
        )

        InscripcionActividad.objects.create(
            vecino=otro_vecino,
            actividad=self.actividad,
        )

        response = self.client.post(
            reverse(
                "actividades:inscribir",
                args=[self.actividad.id],
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            InscripcionActividad.objects.filter(
                vecino=self.vecino,
                actividad=self.actividad,
            ).exists()
        )

        self.assertEqual(
            InscripcionActividad.objects.filter(
                actividad=self.actividad,
            ).count(),
            1,
        )

    def test_actividad_pasada_rechaza_inscripcion(self):
        self.actividad.fecha = timezone.now() - timedelta(days=1)
        self.actividad.save()

        response = self.client.post(
            reverse(
                "actividades:inscribir",
                args=[self.actividad.id],
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            InscripcionActividad.objects.filter(
                vecino=self.vecino,
                actividad=self.actividad,
            ).exists()
        )