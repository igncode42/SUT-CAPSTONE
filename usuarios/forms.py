from django import forms

from vecinos.models import Vecino

from .models import Usuario


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario

        fields = (
            "email",
        )

        labels = {
            "email": "Correo electrónico",
        }

        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "autocomplete": "email",
                    "placeholder": "correo@ejemplo.cl",
                }
            ),
        }


class PerfilVecinoForm(forms.ModelForm):
    class Meta:
        model = Vecino

        fields = (
            "nombre",
            "apellido",
            "direccion",
        )

        labels = {
            "nombre": "Nombre",
            "apellido": "Apellido",
            "direccion": "Dirección",
        }

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "autocomplete": "given-name",
                }
            ),
            "apellido": forms.TextInput(
                attrs={
                    "autocomplete": "family-name",
                }
            ),
            "direccion": forms.TextInput(
                attrs={
                    "autocomplete": "street-address",
                }
            ),
        }