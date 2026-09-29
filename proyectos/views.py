from django.shortcuts import redirect, render

from usuarios.permisos import es_miembro_junta, permiso_requerido

from .forms import ProyectoVecinalForm
from .models import ProyectoVecinal


@permiso_requerido(es_miembro_junta)
def crear_proyecto(request):

    if request.method == "POST":

        form = ProyectoVecinalForm(request.POST)

        if form.is_valid():

            proyecto = form.save(commit=False)

            proyecto.vecino = request.user.vecino

            proyecto.estado = ProyectoVecinal.Estado.PENDIENTE

            proyecto.save()

            return redirect("proyectos:mis_proyectos")

    else:
        form = ProyectoVecinalForm()

    return render(
        request,
        "proyectos/crear.html",
        {
            "form": form,
        },
    )


@permiso_requerido(es_miembro_junta)
def mis_proyectos(request):

    proyectos = (
        ProyectoVecinal.objects
        .filter(vecino=request.user.vecino)
        .order_by("-fecha_postulacion")
    )

    return render(
        request,
        "proyectos/mis_proyectos.html",
        {
            "proyectos": proyectos,
        },
    )
