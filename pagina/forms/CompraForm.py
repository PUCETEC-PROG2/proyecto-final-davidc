from django import forms
from ..models import Compra, Cliente, Propiedad
from django.utils import timezone

class CompraForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Cliente"
    )
    fecha_compra = forms.DateTimeField(
        initial=timezone.now,
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'}
        ),
        label="Fecha de Compra"
    )
    propiedades = forms.ModelMultipleChoiceField(
        queryset=Propiedad.objects.filter(estado='disponible'),
        widget=forms.CheckboxSelectMultiple,
        label="Seleccione las propiedades"
    )

    class Meta:
        model = Compra
        fields = ['cliente', 'fecha_compra', 'propiedades']

