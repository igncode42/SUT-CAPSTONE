from django.shortcuts import get_object_or_404, redirect, render

from usuarios.permisos import (
    permiso_requerido,
    puede_publicar_comunicaciones,
)

from .forms import AvisoForm, NoticiaForm
from .models import Aviso, Noticia


def comunicaciones_inicio(request):
    noticias = (
        Noticia.objects.select_related("usuario")
        .order_by("-fecha_publicacion")
    )

    avisos = (
        Aviso.objects.select_related("usuario")
        .order_by("-fecha_publicacion")
    )

    return render(
        request,
        "comunicaciones/inicio.html",
        {
            "noticias": noticias,
            "avisos": avisos,
            "puede_publicar": puede_publicar_comunicaciones(
                request.user
            ),
        },
    )


@permiso_requerido(puede_publicar_comunicaciones)
def publicar_noticia(request):
    if request.method == "POST":
        form = NoticiaForm(request.POST)

        if form.is_valid():
            noticia = form.save(commit=False)

            noticia.usuario = request.user
            noticia.save()

            return redirect("comunicaciones:inicio")

    else:
        form = NoticiaForm()

    return render(
        request,
        "comunicaciones/publicar_noticia.html",
        {
            "form": form,
        },
    )


@permiso_requerido(puede_publicar_comunicaciones)
def publicar_aviso(request):
    if request.method == "POST":
        form = AvisoForm(request.POST)

        if form.is_valid():
            aviso = form.save(commit=False)

            aviso.usuario = request.user
            aviso.save()

            return redirect("comunicaciones:inicio")

    else:
        form = AvisoForm()

    return render(
        request,
        "comunicaciones/publicar_aviso.html",
        {
            "form": form,
        },
    )


@permiso_requerido(puede_publicar_comunicaciones)
def editar_noticia(request, pk):
    noticia = get_object_or_404(
        Noticia,
        pk=pk,
    )

    if request.method == "POST":
        form = NoticiaForm(
            request.POST,
            instance=noticia,
        )

        if form.is_valid():
            form.save()

            return redirect("comunicaciones:inicio")

    else:
        form = NoticiaForm(
            instance=noticia,
        )

    return render(
        request,
        "comunicaciones/editar_noticia.html",
        {
            "form": form,
            "noticia": noticia,
        },
    )


@permiso_requerido(puede_publicar_comunicaciones)
def eliminar_noticia(request, pk):
    noticia = get_object_or_404(
        Noticia,
        pk=pk,
    )

    if request.method == "POST":
        noticia.delete()

        return redirect("comunicaciones:inicio")

    return render(
        request,
        "comunicaciones/eliminar_noticia.html",
        {
            "noticia": noticia,
        },
    )


@permiso_requerido(puede_publicar_comunicaciones)
def editar_aviso(request, pk):
    aviso = get_object_or_404(
        Aviso,
        pk=pk,
    )

    if request.method == "POST":
        form = AvisoForm(
            request.POST,
            instance=aviso,
        )

        if form.is_valid():
            form.save()

            return redirect("comunicaciones:inicio")

    else:
        form = AvisoForm(
            instance=aviso,
        )

    return render(
        request,
        "comunicaciones/editar_aviso.html",
        {
            "form": form,
            "aviso": aviso,
        },
    )


@permiso_requerido(puede_publicar_comunicaciones)
def eliminar_aviso(request, pk):
    aviso = get_object_or_404(
        Aviso,
        pk=pk,
    )

    if request.method == "POST":
        aviso.delete()

        return redirect("comunicaciones:inicio")

    return render(
        request,
        "comunicaciones/eliminar_aviso.html",
        {
            "aviso": aviso,
        },
    )