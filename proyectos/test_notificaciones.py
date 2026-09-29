from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from usuarios.models import Rol
from vecinos.models import Vecino

from .models import ProyectoVecinal


Usuario = get_user_model()


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
)
class NotificacionProyectoTests(TestCase):

    def crear_proyecto(self, email="vecino@example.com"):

        usuario = Usuario.objects.create_user(
            username="postulante",
            password="ClaveSegura123!",
            email=email,
        )

        vecino = Vecino.objects.create(
            usuario=usuario,
            nombre="Ana",
            apellido="Vecina",
            identificacion="POSTULANTE-1",
            direccion="Dirección de prueba",
            miembro_junta=True,
        )

        return ProyectoVecinal.objects.create(
            vecino=vecino,
            titulo="Mejoramiento plaza",
            descripcion="Proyecto comunitario.",
        )


    def crear_directiva(self):

        rol = Rol.objects.create(
            nombre="Directiva"
        )

        return Usuario.objects.create_user(
            username="directiva",
            password="ClaveSegura123!",
            rol=rol,
        )


    def login_directiva(self):

        directiva = self.crear_directiva()

        self.client.login(
            username=directiva.username,
            password="ClaveSegura123!",
        )


    def test_aprobar_envia_email(self):

        proyecto = self.crear_proyecto()

        self.login_directiva()

        self.client.post(
            reverse(
                "proyectos:resolver",
                args=[
                    proyecto.pk,
                    "aprobar",
                ],
            )
        )

        self.assertEqual(
            len(mail.outbox),
            1,
        )

        correo = mail.outbox[0]

        self.assertEqual(
            correo.to,
            ["vecino@example.com"],
        )

        self.assertIn(
            "Mejoramiento plaza",
            correo.subject,
        )

        self.assertIn(
            "Aprobado",
            correo.body,
        )


    def test_rechazar_envia_email(self):

        proyecto = self.crear_proyecto()

        self.login_directiva()

        self.client.post(
            reverse(
                "proyectos:resolver",
                args=[
                    proyecto.pk,
                    "rechazar",
                ],
            )
        )

        self.assertEqual(
            len(mail.outbox),
            1,
        )

        self.assertIn(
            "Rechazado",
            mail.outbox[0].body,
        )


    def test_sin_email_no_falla(self):

        proyecto = self.crear_proyecto(
            email=""
        )

        self.login_directiva()

        response = self.client.post(
            reverse(
                "proyectos:resolver",
                args=[
                    proyecto.pk,
                    "aprobar",
                ],
            )
        )

        self.assertRedirects(
            response,
            reverse("proyectos:pendientes"),
        )

        self.assertEqual(
            len(mail.outbox),
            0,
        )


    def test_no_envia_segundo_email_si_ya_esta_resuelto(self):

        proyecto = self.crear_proyecto()

        self.login_directiva()

        self.client.post(
            reverse(
                "proyectos:resolver",
                args=[
                    proyecto.pk,
                    "aprobar",
                ],
            )
        )

        response = self.client.post(
            reverse(
                "proyectos:resolver",
                args=[
                    proyecto.pk,
                    "rechazar",
                ],
            )
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertEqual(
            len(mail.outbox),
            1,
        )

        proyecto.refresh_from_db()

        self.assertEqual(
            proyecto.estado,
            ProyectoVecinal.Estado.APROBADO,
        )
