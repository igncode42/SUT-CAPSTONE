from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from django.contrib.auth.views import redirect_to_login


def es_vecino(usuario):
    if not usuario.is_authenticated:
        return False

    return hasattr(usuario, "vecino")


def es_miembro_junta(usuario):
    if not es_vecino(usuario):
        return False

    return usuario.vecino.miembro_junta


def tiene_rol(usuario, *nombres):
    if not usuario.is_authenticated:
        return False

    rol = getattr(usuario, "rol", None)

    if rol is None:
        return False

    permitidos = {
        nombre.strip().casefold()
        for nombre in nombres
    }

    return rol.nombre.strip().casefold() in permitidos


def permiso_requerido(verificador):
    def decorador(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect_to_login(
                    request.get_full_path(),
                    resolve_url("login"),
                )

            if not verificador(request.user):
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorador


def puede_resolver_proyectos(usuario):
    if not usuario.is_authenticated:
        return False

    if usuario.is_superuser or usuario.is_staff:
        return True

    return tiene_rol(
        usuario,
        "directiva",
        "personal autorizado",
    )
