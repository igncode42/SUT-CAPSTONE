from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from usuarios.models import Rol
from vecinos.models import Vecino

from .models import Actividad, InscripcionActividad


Usuario = get_user_model()


# ============================================================
# FLUJO DEL VECINO
# ============================================================


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

        self.assertEqual(
            response.status_code,
            200,
        )

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

        self.assertEqual(
            response.status_code,
            302,
        )

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

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertEqual(
            InscripcionActividad.objects.filter(
                vecino=self.vecino,
                actividad=self.actividad,
            ).count(),
            1,
        )


    def test_bd_impide_inscripcion_duplicada(self):

        InscripcionActividad.objects.create(
            vecino=self.vecino,
            actividad=self.actividad,
        )

        with self.assertRaises(IntegrityError):

            with transaction.atomic():

                InscripcionActividad.objects.create(
                    vecino=self.vecino,
                    actividad=self.actividad,
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

        self.assertEqual(
            response.status_code,
            302,
        )

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


    def test_cupo_maximo_cero_es_invalido(self):

        actividad = Actividad(
            nombre="Actividad inválida",
            fecha=timezone.now() + timedelta(days=1),
            cupo_maximo=0,
        )

        with self.assertRaises(ValidationError):
            actividad.full_clean()


    def test_actividad_pasada_rechaza_inscripcion(self):

        self.actividad.fecha = (
            timezone.now()
            - timedelta(days=1)
        )

        self.actividad.save()

        response = self.client.post(
            reverse(
                "actividades:inscribir",
                args=[self.actividad.id],
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertFalse(
            InscripcionActividad.objects.filter(
                vecino=self.vecino,
                actividad=self.actividad,
            ).exists()
        )


# ============================================================
# GESTION ADMINISTRATIVA
# ============================================================


class GestionActividadTests(TestCase):

    def setUp(self):

        self.rol_directiva, _ = Rol.objects.get_or_create(
            nombre="Directiva"
        )

        self.rol_autorizado, _ = Rol.objects.get_or_create(
            nombre="Personal autorizado"
        )

        self.directiva = Usuario.objects.create_user(
            username="directiva_actividades",
            password="SUT-Directiva-2026!",
            rol=self.rol_directiva,
        )

        self.autorizado = Usuario.objects.create_user(
            username="autorizado_actividades",
            password="SUT-Autorizado-2026!",
            rol=self.rol_autorizado,
        )

        self.usuario_vecino = Usuario.objects.create_user(
            username="vecino_sin_gestion",
            password="SUT-Vecino-2026!",
        )

        self.vecino = Vecino.objects.create(
            usuario=self.usuario_vecino,
            nombre="Vecino",
            apellido="Sin Gestión",
            identificacion="SUT-ACT-GEST-001",
            direccion="Calle Gestión 100",
            miembro_junta=False,
        )

        self.usuario_miembro = Usuario.objects.create_user(
            username="miembro_sin_gestion",
            password="SUT-Miembro-2026!",
        )

        self.miembro = Vecino.objects.create(
            usuario=self.usuario_miembro,
            nombre="Miembro",
            apellido="Junta",
            identificacion="SUT-ACT-GEST-002",
            direccion="Calle Junta 200",
            miembro_junta=True,
        )

        self.actividad = Actividad.objects.create(
            nombre="Actividad Administrable",
            descripcion="Actividad para probar el CRUD.",
            fecha=timezone.now() + timedelta(days=5),
            cupo_maximo=10,
        )


    def fecha_formulario(self, dias=7):

        fecha = timezone.localtime(
            timezone.now() + timedelta(days=dias)
        )

        return fecha.strftime(
            "%Y-%m-%dT%H:%M"
        )


    def test_directiva_puede_ver_gestion_actividades(self):

        self.client.force_login(
            self.directiva
        )

        response = self.client.get(
            reverse("actividades:gestion")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "actividades/gestion.html",
        )

        self.assertContains(
            response,
            "Actividad Administrable",
        )


    def test_personal_autorizado_puede_ver_gestion_actividades(self):

        self.client.force_login(
            self.autorizado
        )

        response = self.client.get(
            reverse("actividades:gestion")
        )

        self.assertEqual(
            response.status_code,
            200,
        )


    def test_vecino_no_puede_gestionar_actividades(self):

        self.client.force_login(
            self.usuario_vecino
        )

        response = self.client.get(
            reverse("actividades:gestion")
        )

        self.assertEqual(
            response.status_code,
            403,
        )


    def test_miembro_junta_no_puede_gestionar_actividades(self):

        self.client.force_login(
            self.usuario_miembro
        )

        response = self.client.get(
            reverse("actividades:gestion")
        )

        self.assertEqual(
            response.status_code,
            403,
        )


    def test_directiva_puede_crear_actividad(self):

        self.client.force_login(
            self.directiva
        )

        response = self.client.post(
            reverse("actividades:crear"),
            {
                "nombre": "Nueva actividad",
                "descripcion": "Creada desde gestión.",
                "fecha": self.fecha_formulario(),
                "cupo_maximo": 25,
            },
        )

        self.assertRedirects(
            response,
            reverse("actividades:gestion"),
        )

        self.assertTrue(
            Actividad.objects.filter(
                nombre="Nueva actividad"
            ).exists()
        )


    def test_directiva_puede_editar_actividad(self):

        self.client.force_login(
            self.directiva
        )

        response = self.client.post(
            reverse(
                "actividades:editar",
                args=[self.actividad.id],
            ),
            {
                "nombre": "Actividad actualizada",
                "descripcion": "Descripción actualizada.",
                "fecha": self.fecha_formulario(),
                "cupo_maximo": 30,
            },
        )

        self.assertRedirects(
            response,
            reverse("actividades:gestion"),
        )

        self.actividad.refresh_from_db()

        self.assertEqual(
            self.actividad.nombre,
            "Actividad actualizada",
        )

        self.assertEqual(
            self.actividad.cupo_maximo,
            30,
        )


    def test_no_permite_reducir_cupo_bajo_inscritos_actuales(self):

        usuario_inscrito = Usuario.objects.create_user(
            username="vecino_inscrito_gestion",
            password="SUT-Inscrito-2026!",
        )

        vecino_inscrito = Vecino.objects.create(
            usuario=usuario_inscrito,
            nombre="Vecino",
            apellido="Inscrito",
            identificacion="SUT-ACT-GEST-003",
            direccion="Calle Inscrito 300",
        )

        InscripcionActividad.objects.create(
            vecino=vecino_inscrito,
            actividad=self.actividad,
        )

        segundo_usuario = Usuario.objects.create_user(
            username="vecino_inscrito_gestion_2",
            password="SUT-Inscrito2-2026!",
        )

        segundo_vecino = Vecino.objects.create(
            usuario=segundo_usuario,
            nombre="Segundo",
            apellido="Inscrito",
            identificacion="SUT-ACT-GEST-004",
            direccion="Calle Inscrito 400",
        )

        InscripcionActividad.objects.create(
            vecino=segundo_vecino,
            actividad=self.actividad,
        )

        self.client.force_login(
            self.directiva
        )

        response = self.client.post(
            reverse(
                "actividades:editar",
                args=[self.actividad.id],
            ),
            {
                "nombre": self.actividad.nombre,
                "descripcion": self.actividad.descripcion,
                "fecha": self.fecha_formulario(),
                "cupo_maximo": 1,
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.actividad.refresh_from_db()

        self.assertEqual(
            self.actividad.cupo_maximo,
            10,
        )

        self.assertFormError(
            response.context["form"],
            "cupo_maximo",
            (
                "El cupo máximo no puede ser menor "
                "que los 2 vecinos actualmente inscritos."
            ),
        )


    def test_directiva_puede_eliminar_actividad_sin_inscritos(self):

        self.client.force_login(
            self.directiva
        )

        actividad_id = self.actividad.id

        response = self.client.post(
            reverse(
                "actividades:eliminar",
                args=[actividad_id],
            )
        )

        self.assertRedirects(
            response,
            reverse("actividades:gestion"),
        )

        self.assertFalse(
            Actividad.objects.filter(
                pk=actividad_id
            ).exists()
        )


    def test_no_permite_eliminar_actividad_con_inscritos(self):

        usuario_inscrito = Usuario.objects.create_user(
            username="vecino_protegido",
            password="SUT-Protegido-2026!",
        )

        vecino_inscrito = Vecino.objects.create(
            usuario=usuario_inscrito,
            nombre="Vecino",
            apellido="Protegido",
            identificacion="SUT-ACT-GEST-005",
            direccion="Calle Protegida 500",
        )

        InscripcionActividad.objects.create(
            vecino=vecino_inscrito,
            actividad=self.actividad,
        )

        self.client.force_login(
            self.directiva
        )

        response = self.client.post(
            reverse(
                "actividades:eliminar",
                args=[self.actividad.id],
            )
        )

        self.assertRedirects(
            response,
            reverse("actividades:gestion"),
        )

        self.assertTrue(
            Actividad.objects.filter(
                pk=self.actividad.id
            ).exists()
        )

        self.assertTrue(
            InscripcionActividad.objects.filter(
                actividad=self.actividad,
                vecino=vecino_inscrito,
            ).exists()
        )