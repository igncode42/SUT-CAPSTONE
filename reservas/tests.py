from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
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

        self.fecha = (
            timezone.localdate()
            + timedelta(days=1)
        )

        self.client.login(
            username="vecino_reservas",
            password="SUT-Reserva-2026!",
        )


    def test_mis_reservas_responde_200(self):

        response = self.client.get(
            reverse("reservas:mis_reservas")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "reservas/mis_reservas.html",
        )


    def test_reserva_valida_se_confirma_para_vecino_autenticado(self):

        response = self.client.post(
            reverse("reservas:crear"),
            {
                "espacio": self.espacio.id,
                "fecha": self.fecha,
                "hora_inicio": "15:00",
                "hora_fin": "17:00",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        reserva = Reserva.objects.get()

        self.assertEqual(
            reserva.vecino,
            self.vecino,
        )

        self.assertEqual(
            reserva.espacio,
            self.espacio,
        )

        self.assertEqual(
            reserva.estado,
            Reserva.Estado.CONFIRMADA,
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

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            Reserva.objects.count(),
            0,
        )

        self.assertContains(
            response,
            "La hora de término debe ser posterior a la hora de inicio.",
        )


    def test_bd_rechaza_horario_invalido(self):

        with self.assertRaises(IntegrityError):

            with transaction.atomic():

                Reserva.objects.create(
                    vecino=self.vecino,
                    espacio=self.espacio,
                    fecha=self.fecha,
                    hora_inicio="18:00",
                    hora_fin="16:00",
                    estado=Reserva.Estado.CONFIRMADA,
                )


    def test_bd_rechaza_estado_invalido(self):

        with self.assertRaises(IntegrityError):

            with transaction.atomic():

                Reserva.objects.create(
                    vecino=self.vecino,
                    espacio=self.espacio,
                    fecha=self.fecha,
                    hora_inicio="15:00",
                    hora_fin="17:00",
                    estado="ESTADO_INVENTADO",
                )


    def test_reserva_solapada_es_rechazada(self):

        Reserva.objects.create(
            vecino=self.vecino,
            espacio=self.espacio,
            fecha=self.fecha,
            hora_inicio="15:00",
            hora_fin="17:00",
            estado=Reserva.Estado.CONFIRMADA,
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

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            Reserva.objects.count(),
            1,
        )

        self.assertContains(
            response,
            "El espacio ya está reservado durante parte de ese horario.",
        )


    def test_horarios_contiguos_no_se_solapan(self):

        Reserva.objects.create(
            vecino=self.vecino,
            espacio=self.espacio,
            fecha=self.fecha,
            hora_inicio="10:00",
            hora_fin="12:00",
            estado=Reserva.Estado.CONFIRMADA,
        )

        response = self.client.post(
            reverse("reservas:crear"),
            {
                "espacio": self.espacio.id,
                "fecha": self.fecha,
                "hora_inicio": "12:00",
                "hora_fin": "14:00",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertEqual(
            Reserva.objects.count(),
            2,
        )


    def test_espacio_inactivo_no_puede_reservarse(self):

        espacio_inactivo = Espacio.objects.create(
            nombre="Espacio fuera de servicio",
            activo=False,
        )

        response = self.client.post(
            reverse("reservas:crear"),
            {
                "espacio": espacio_inactivo.id,
                "fecha": self.fecha,
                "hora_inicio": "10:00",
                "hora_fin": "12:00",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            Reserva.objects.count(),
            0,
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
            estado=Reserva.Estado.CONFIRMADA,
        )

        response = self.client.get(
            reverse("reservas:mis_reservas")
        )

        self.assertNotContains(
            response,
            "10:00",
        )


    def test_calendario_responde_200(self):

        response = self.client.get(
            reverse("reservas:calendario")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "reservas/calendario.html",
        )


    def test_calendario_muestra_reserva_confirmada(self):

        Reserva.objects.create(
            vecino=self.vecino,
            espacio=self.espacio,
            fecha=self.fecha,
            hora_inicio="15:00",
            hora_fin="17:00",
            estado=Reserva.Estado.CONFIRMADA,
        )

        response = self.client.get(
            reverse("reservas:calendario"),
            {
                "mes": self.fecha.month,
                "anio": self.fecha.year,
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Sede Social",
        )


    def test_calendario_no_muestra_reserva_cancelada(self):

        espacio_cancelado = Espacio.objects.create(
            nombre="Sala Cancelada",
            activo=True,
        )

        Reserva.objects.create(
            vecino=self.vecino,
            espacio=espacio_cancelado,
            fecha=self.fecha,
            hora_inicio="12:00",
            hora_fin="13:00",
            estado=Reserva.Estado.CANCELADA,
        )

        response = self.client.get(
            reverse("reservas:calendario"),
            {
                "mes": self.fecha.month,
                "anio": self.fecha.year,
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertNotContains(
            response,
            "Sala Cancelada",
        )


    def test_calendario_parametros_invalidos_no_provocan_error(self):

        response = self.client.get(
            reverse("reservas:calendario"),
            {
                "mes": "99",
                "anio": "100000000",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.context["mes"],
            timezone.localdate().month,
        )

        self.assertEqual(
            response.context["anio"],
            timezone.localdate().year,
        )