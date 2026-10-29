from django.shortcuts import redirect, render

from usuarios.permisos import es_vecino, permiso_requerido

from .forms import ReservaForm
from .models import Reserva


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