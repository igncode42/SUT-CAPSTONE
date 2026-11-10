from django import forms

from .models import Actividad


class ActividadForm(forms.ModelForm):

    class Meta:
        model = Actividad

        fields = [
            "nombre",
            "descripcion",
            "fecha",
            "cupo_maximo",
        ]

        labels = {
            "nombre": "Nombre de la actividad",
            "descripcion": "Descripción",
            "fecha": "Fecha y hora",
            "cupo_maximo": "Cupo máximo",
        }

        help_texts = {
            "descripcion": (
                "Describe brevemente en qué consiste la actividad."
            ),
            "fecha": (
                "Selecciona la fecha y hora en que se realizará."
            ),
            "cupo_maximo": (
                "Cantidad máxima de vecinos que podrán inscribirse."
            ),
        }

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. Taller de actividad física",
                    "autocomplete": "off",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": (
                        "Describe la actividad para los vecinos."
                    ),
                }
            ),
            "fecha": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
            ),
            "cupo_maximo": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "step": 1,
                    "placeholder": "Ej. 20",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["fecha"].input_formats = [
            "%Y-%m-%dT%H:%M",
        ]