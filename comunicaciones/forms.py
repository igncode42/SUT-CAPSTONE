from django import forms

from .models import Aviso, Noticia


class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = (
            "titulo",
            "contenido",
        )
        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "contenido": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                }
            ),
        }


class AvisoForm(forms.ModelForm):
    class Meta:
        model = Aviso
        fields = (
            "titulo",
            "contenido",
        )
        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "contenido": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                }
            ),
        }