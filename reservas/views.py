from calendar import monthcalendar
from datetime import date

from django.shortcuts import redirect, render
from django.utils import timezone

from usuarios.permisos import es_vecino, permiso_requerido

from .forms import ReservaForm
from .models import Reserva


MESES = (
    "",
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
)


@permiso_requerido(es_vecino)
def mis_reservas(request):
    reservas = Reserva.objects.filter(
        vecino=request.user.vecino
    ).select_related("espacio").order_by(
        "-fecha",
        "-hora_inicio",
    )

    return render(
        request,
        "reservas/mis_reservas.html",
        {
            "reservas": reservas,
        },
    )


@permiso_requerido(es_vecino)
def crear_reserva(request):
    if request.method == "POST":
        form = ReservaForm(request.POST)

        if form.is_valid():
            reserva = form.save(commit=False)

            reserva.vecino = request.user.vecino
            reserva.estado = Reserva.Estado.CONFIRMADA
            reserva.save()

            return redirect("reservas:mis_reservas")

    else:
        form = ReservaForm()

    return render(
        request,
        "reservas/crear_reserva.html",
        {
            "form": form,
        },
    )


@permiso_requerido(es_vecino)
def calendario(request):
    hoy = timezone.localdate()

    try:
        anio = int(request.GET.get("anio", hoy.year))
        mes = int(request.GET.get("mes", hoy.month))
    except (TypeError, ValueError):
        anio = hoy.year
        mes = hoy.month

    if mes < 1 or mes > 12:
        anio = hoy.year
        mes = hoy.month

    reservas_mes = (
        Reserva.objects.filter(
            fecha__year=anio,
            fecha__month=mes,
        )
        .exclude(
            estado=Reserva.Estado.CANCELADA,
        )
        .select_related("espacio")
        .order_by(
            "fecha",
            "hora_inicio",
        )
    )

    reservas_por_fecha = {}

    for reserva in reservas_mes:
        reservas_por_fecha.setdefault(
            reserva.fecha,
            [],
        ).append(reserva)

    semanas = []

    for semana in monthcalendar(anio, mes):
        dias = []

        for numero_dia in semana:
            if numero_dia == 0:
                dias.append(None)
                continue

            fecha_dia = date(
                anio,
                mes,
                numero_dia,
            )

            dias.append(
                {
                    "fecha": fecha_dia,
                    "numero": numero_dia,
                    "es_hoy": fecha_dia == hoy,
                    "reservas": reservas_por_fecha.get(
                        fecha_dia,
                        [],
                    ),
                }
            )

        semanas.append(dias)

    if mes == 1:
        mes_anterior = 12
        anio_anterior = anio - 1
    else:
        mes_anterior = mes - 1
        anio_anterior = anio

    if mes == 12:
        mes_siguiente = 1
        anio_siguiente = anio + 1
    else:
        mes_siguiente = mes + 1
        anio_siguiente = anio

    return render(
        request,
        "reservas/calendario.html",
        {
            "semanas": semanas,
            "mes_nombre": MESES[mes],
            "mes": mes,
            "anio": anio,
            "mes_anterior": mes_anterior,
            "anio_anterior": anio_anterior,
            "mes_siguiente": mes_siguiente,
            "anio_siguiente": anio_siguiente,
        },
    )