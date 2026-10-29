from django import forms
from django.utils import timezone

from .models import Espacio, Reserva


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = (
            "espacio",
            "fecha",
            "hora_inicio",
            "hora_fin",
        )
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "hora_inicio": forms.TimeInput(attrs={"type": "time"}),
            "hora_fin": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["espacio"].queryset = Espacio.objects.filter(
            activo=True
        )

    def clean(self):
        cleaned_data = super().clean()

        espacio = cleaned_data.get("espacio")
        fecha = cleaned_data.get("fecha")
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fin = cleaned_data.get("hora_fin")

        if fecha and fecha < timezone.localdate():
            self.add_error(
                "fecha",
                "No puedes reservar una fecha pasada.",
            )

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            self.add_error(
                "hora_fin",
                "La hora de término debe ser posterior a la hora de inicio.",
            )

        if espacio and fecha and hora_inicio and hora_fin:
            existe_solapamiento = Reserva.objects.filter(
                espacio=espacio,
                fecha=fecha,
            ).exclude(
                estado=Reserva.Estado.CANCELADA
            ).filter(
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio,
            ).exists()

            if existe_solapamiento:
                raise forms.ValidationError(
                    "El espacio ya está reservado durante parte de ese horario."
                )

        return cleaned_data