from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from usuarios.permisos import es_vecino, permiso_requerido

from .models import Actividad, InscripcionActividad


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