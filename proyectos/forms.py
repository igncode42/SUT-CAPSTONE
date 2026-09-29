from django import forms

from .models import ProyectoVecinal


class ProyectoVecinalForm(forms.ModelForm):

    class Meta:
        model = ProyectoVecinal

        fields = [
            "titulo",
            "descripcion",
        ]

        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del proyecto",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe el proyecto vecinal",
                }
            ),
        }
