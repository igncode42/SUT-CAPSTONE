from django.contrib import messages
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from usuarios.permisos import (
    es_vecino,
    permiso_requerido,
    puede_gestionar_actividades,
)

from .forms import ActividadForm
from .models import Actividad, InscripcionActividad


# ============================================================
# VECINOS
# ============================================================


@permiso_requerido(es_vecino)
def actividades_disponibles(request):
    actividades = (
        Actividad.objects.filter(
            fecha__gte=timezone.now()
        )
        .annotate(
            cantidad_inscritos=Count("inscripciones")
        )
        .order_by("fecha")
    )

    inscripciones_usuario = set(
        InscripcionActividad.objects.filter(
            vecino=request.user.vecino
        ).values_list(
            "actividad_id",
            flat=True,
        )
    )

    return render(
        request,
        "actividades/disponibles.html",
        {
            "actividades": actividades,
            "inscripciones_usuario": inscripciones_usuario,
        },
    )


@permiso_requerido(es_vecino)
def mis_actividades(request):
    inscripciones = (
        InscripcionActividad.objects.filter(
            vecino=request.user.vecino
        )
        .select_related("actividad")
        .order_by("actividad__fecha")
    )

    return render(
        request,
        "actividades/mis_actividades.html",
        {
            "inscripciones": inscripciones,
        },
    )


@permiso_requerido(es_vecino)
def inscribir_actividad(request, actividad_id):
    if request.method != "POST":
        return redirect("actividades:disponibles")

    with transaction.atomic():
        actividad = get_object_or_404(
            Actividad.objects.select_for_update(),
            pk=actividad_id,
        )

        if actividad.fecha <= timezone.now():
            return redirect("actividades:disponibles")

        ya_inscrito = InscripcionActividad.objects.filter(
            vecino=request.user.vecino,
            actividad=actividad,
        ).exists()

        if ya_inscrito:
            return redirect("actividades:disponibles")

        inscritos = InscripcionActividad.objects.filter(
            actividad=actividad
        ).count()

        if inscritos >= actividad.cupo_maximo:
            return redirect("actividades:disponibles")

        InscripcionActividad.objects.create(
            vecino=request.user.vecino,
            actividad=actividad,
        )

    return redirect("actividades:mis_actividades")


# ============================================================
# GESTION ADMINISTRATIVA
# ============================================================


@permiso_requerido(puede_gestionar_actividades)
def gestion_actividades(request):
    actividades = (
        Actividad.objects
        .annotate(
            cantidad_inscritos=Count("inscripciones")
        )
        .order_by("-fecha")
    )

    return render(
        request,
        "actividades/gestion.html",
        {
            "actividades": actividades,
            "ahora": timezone.now(),
        },
    )


@permiso_requerido(puede_gestionar_actividades)
def crear_actividad(request):
    if request.method == "POST":
        form = ActividadForm(request.POST)

        if form.is_valid():

            if form.cleaned_data["fecha"] <= timezone.now():
                form.add_error(
                    "fecha",
                    "La actividad debe programarse para una fecha futura.",
                )

            else:
                actividad = form.save()

                messages.success(
                    request,
                    (
                        f'La actividad "{actividad.nombre}" '
                        "fue creada correctamente."
                    ),
                )

                return redirect(
                    "actividades:gestion"
                )

    else:
        form = ActividadForm()

    return render(
        request,
        "actividades/formulario.html",
        {
            "form": form,
            "titulo": "Crear actividad",
            "texto_boton": "Crear actividad",
        },
    )


@permiso_requerido(puede_gestionar_actividades)
def editar_actividad(request, actividad_id):
    actividad = get_object_or_404(
        Actividad,
        pk=actividad_id,
    )

    if request.method == "POST":

        with transaction.atomic():

            actividad = get_object_or_404(
                Actividad.objects.select_for_update(),
                pk=actividad_id,
            )

            form = ActividadForm(
                request.POST,
                instance=actividad,
            )

            if form.is_valid():

                cantidad_inscritos = (
                    InscripcionActividad.objects.filter(
                        actividad=actividad
                    ).count()
                )

                nuevo_cupo = form.cleaned_data[
                    "cupo_maximo"
                ]

                nueva_fecha = form.cleaned_data[
                    "fecha"
                ]

                if nueva_fecha <= timezone.now():

                    form.add_error(
                        "fecha",
                        (
                            "La actividad debe programarse "
                            "para una fecha futura."
                        ),
                    )

                elif nuevo_cupo < cantidad_inscritos:

                    form.add_error(
                        "cupo_maximo",
                        (
                            "El cupo máximo no puede ser menor "
                            f"que los {cantidad_inscritos} "
                            "vecinos actualmente inscritos."
                        ),
                    )

                else:
                    actividad = form.save()

                    messages.success(
                        request,
                        (
                            f'La actividad "{actividad.nombre}" '
                            "fue actualizada correctamente."
                        ),
                    )

                    return redirect(
                        "actividades:gestion"
                    )

    else:
        form = ActividadForm(
            instance=actividad
        )

    return render(
        request,
        "actividades/formulario.html",
        {
            "form": form,
            "actividad": actividad,
            "titulo": "Editar actividad",
            "texto_boton": "Guardar cambios",
        },
    )


@permiso_requerido(puede_gestionar_actividades)
def eliminar_actividad(request, actividad_id):
    actividad = get_object_or_404(
        Actividad,
        pk=actividad_id,
    )

    cantidad_inscritos = (
        InscripcionActividad.objects.filter(
            actividad=actividad
        ).count()
    )

    if request.method == "POST":

        with transaction.atomic():

            actividad = get_object_or_404(
                Actividad.objects.select_for_update(),
                pk=actividad_id,
            )

            cantidad_inscritos = (
                InscripcionActividad.objects.filter(
                    actividad=actividad
                ).count()
            )

            if cantidad_inscritos > 0:

                messages.error(
                    request,
                    (
                        "No se puede eliminar la actividad "
                        "porque tiene vecinos inscritos."
                    ),
                )

                return redirect(
                    "actividades:gestion"
                )

            nombre_actividad = actividad.nombre

            actividad.delete()

            messages.success(
                request,
                (
                    f'La actividad "{nombre_actividad}" '
                    "fue eliminada correctamente."
                ),
            )

            return redirect(
                "actividades:gestion"
            )

    return render(
        request,
        "actividades/eliminar.html",
        {
            "actividad": actividad,
            "cantidad_inscritos": cantidad_inscritos,
        },
    )