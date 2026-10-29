from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from vecinos.models import Vecino

from .models import Espacio, Reserva


Usuario = get_user_model()


class ReservaTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="vecino_reservas",
            password="SUT-Reserva-2026!",
        )

        self.vecino = Vecino.objects.create(
            usuario=self.usuario,
            nombre="Vecino",
            apellido="Reservas",
            identificacion="SUT-RESERVAS-001",
            direccion="Calle Reserva 123",
        )

        self.espacio = Espacio.objects.create(
            nombre="Sede Social",
            activo=True,
        )

        self.fecha = timezone.localdate() + timedelta(days=1)

        self.client.login(
            username="vecino_reservas",
            password="SUT-Reserva-2026!",
        )

    def test_mis_reservas_responde_200(self):
        response = self.client.get(
            reverse("reservas:mis_reservas")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "reservas/mis_reservas.html",
        )

    def test_reserva_valida_se_crea_para_vecino_autenticado(self):
        response = self.client.post(
            reverse("reservas:crear"),
            {
                "espacio": self.espacio.id,
                "fecha": self.fecha,
                "hora_inicio": "15:00",
                "hora_fin": "17:00",
            },
        )

        self.assertEqual(response.status_code, 302)

        reserva = Reserva.objects.get()

        self.assertEqual(reserva.vecino, self.vecino)
        self.assertEqual(reserva.espacio, self.espacio)
        self.assertEqual(
            reserva.estado,
            Reserva.Estado.PENDIENTE,
        )

    def test_horario_invalido_es_rechazado(self):
        response = self.client.post(
            reverse("reservas:crear"),
            {
                "espacio": self.espacio.id,
                "fecha": self.fecha,
                "hora_inicio": "18:00",
                "hora_fin": "16:00",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reserva.objects.count(), 0)

        self.assertContains(
            response,
            "La hora de término debe ser posterior a la hora de inicio.",
        )

    def test_reserva_solapada_es_rechazada(self):
        Reserva.objects.create(
            vecino=self.vecino,
            espacio=self.espacio,
            fecha=self.fecha,
            hora_inicio="15:00",
            hora_fin="17:00",
        )

        response = self.client.post(
            reverse("reservas:crear"),
            {
                "espacio": self.espacio.id,
                "fecha": self.fecha,
                "hora_inicio": "16:00",
                "hora_fin": "18:00",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reserva.objects.count(), 1)

        self.assertContains(
            response,
            "El espacio ya está reservado durante parte de ese horario.",
        )

    def test_vecino_solo_ve_sus_propias_reservas(self):
        otro_usuario = Usuario.objects.create_user(
            username="otro_vecino",
            password="SUT-Otro-2026!",
        )

        otro_vecino = Vecino.objects.create(
            usuario=otro_usuario,
            nombre="Otro",
            apellido="Vecino",
            identificacion="SUT-RESERVAS-002",
            direccion="Otra Calle 456",
        )

        Reserva.objects.create(
            vecino=otro_vecino,
            espacio=self.espacio,
            fecha=self.fecha,
            hora_inicio="10:00",
            hora_fin="11:00",
        )

        response = self.client.get(
            reverse("reservas:mis_reservas")
        )

        self.assertNotContains(
            response,
            "10:00",
        )