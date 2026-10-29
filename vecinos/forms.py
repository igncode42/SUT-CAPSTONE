from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Vecino


Usuario = get_user_model()


class RegistroVecinoForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    identificacion = forms.CharField(max_length=30)
    direccion = forms.CharField(max_length=255)

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = (
            "username",
            "email",
            "nombre",
            "apellido",
            "identificacion",
            "direccion",
            "password1",
            "password2",
        )

    def clean_identificacion(self):
        identificacion = self.cleaned_data["identificacion"].strip()

        if Vecino.objects.filter(identificacion=identificacion).exists():
            raise forms.ValidationError(
                "Ya existe un vecino registrado con esta identificación."
            )

        return identificacion