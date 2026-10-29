from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import RegistroVecinoForm
from .models import Vecino


def registro_vecino(request):
    if request.method == "POST":
        form = RegistroVecinoForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                usuario = form.save()

                Vecino.objects.create(
                    usuario=usuario,
                    nombre=form.cleaned_data["nombre"],
                    apellido=form.cleaned_data["apellido"],
                    identificacion=form.cleaned_data["identificacion"],
                    direccion=form.cleaned_data["direccion"],
                )

            messages.success(
                request,
                "Registro completado correctamente. Ya puedes iniciar sesión.",
            )

            return redirect("login")

    else:
        form = RegistroVecinoForm()

    return render(
        request,
        "vecinos/registro.html",
        {
            "form": form,
        },
    )