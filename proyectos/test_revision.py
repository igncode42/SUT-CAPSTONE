from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from usuarios.models import Rol
from vecinos.models import Vecino

from .models import ProyectoVecinal


Usuario = get_user_model()


class ResolucionProyectoTests(TestCase):

    def crear_usuario(self, username, rol=None):

        return Usuario.objects.create_user(
            username=username,
            password="ClaveSegura123!",
            rol=rol,
        )


    def crear_vecino(
        self,
        usuario,
        miembro_junta=False,
    ):

        return Vecino.objects.create(
            usuario=usuario,
            nombre="Nombre",
            apellido="Prueba",
            identificacion=f"ID-{usuario.username}",
            direccion="Dirección de prueba",
            miembro_junta=miembro_junta,
        )


    def crear_proyecto_pendiente(self):

        usuario = self.crear_usuario("postulante")

        vecino = self.crear_vecino(
            usuario,
            miembro_junta=True,
        )

        return ProyectoVecinal.objects.create(
            vecino=vecino,
            titulo="Proyecto pendiente",
            descripcion="Proyecto para revisión.",
        )


    def login(self, username):

        return self.client.login(
            username=username,
            password="ClaveSegura123!",
        )


    def crear_directiva(self):

        rol = Rol.objects.create(
            nombre="Directiva"
        )

        return self.crear_usuario(
            "directiva",
            rol=rol,
        )


    def test_anonimo_no_puede_ver_pendientes(self):

        response = self.client.get(
            reverse("proyectos:pendientes")
        )

        self.assertEqual(
            response.status_code,
            302,
        )


    def test_miembro_junta_no_puede_resolver(self):

        usuario = self.crear_usuario("miembro")

        self.crear_vecino(
            usuario,
            miembro_junta=True,
        )

        self.login(usuario.username)

        response = self.client.get(
            reverse("proyectos:pendientes")
        )

        self.assertEqual(
            response.status_code,
            403,
        )


    def test_directiva_puede_ver_pendientes(self):

        proyecto = self.crear_proyecto_pendiente()
        directiva = self.crear_directiva()

        self.login(directiva.username)

        response = self.client.get(
            reverse("proyectos:pendientes")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            proyecto.titulo,
        )


    def test_directiva_puede_aprobar(self):

        proyecto = self.crear_proyecto_pendiente()
        directiva = self.crear_directiva()

        self.login(directiva.username)

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

        proyecto.refresh_from_db()

        self.assertEqual(
            proyecto.estado,
            ProyectoVecinal.Estado.APROBADO,
        )


    def test_directiva_puede_rechazar(self):

        proyecto = self.crear_proyecto_pendiente()
        directiva = self.crear_directiva()

        self.login(directiva.username)

        self.client.post(
            reverse(
                "proyectos:resolver",
                args=[
                    proyecto.pk,
                    "rechazar",
                ],
            )
        )

        proyecto.refresh_from_db()

        self.assertEqual(
            proyecto.estado,
            ProyectoVecinal.Estado.RECHAZADO,
        )


    def test_vecino_no_puede_aprobar(self):

        proyecto = self.crear_proyecto_pendiente()

        usuario = self.crear_usuario("vecino")

        self.crear_vecino(
            usuario,
            miembro_junta=False,
        )

        self.login(usuario.username)

        response = self.client.post(
            reverse(
                "proyectos:resolver",
                args=[
                    proyecto.pk,
                    "aprobar",
                ],
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        proyecto.refresh_from_db()

        self.assertEqual(
            proyecto.estado,
            ProyectoVecinal.Estado.PENDIENTE,
        )


    def test_proyecto_resuelto_no_puede_resolverse_de_nuevo(self):

        proyecto = self.crear_proyecto_pendiente()

        proyecto.estado = ProyectoVecinal.Estado.APROBADO
        proyecto.save()

        directiva = self.crear_directiva()

        self.login(directiva.username)

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

        proyecto.refresh_from_db()

        self.assertEqual(
            proyecto.estado,
            ProyectoVecinal.Estado.APROBADO,
        )
