from django import forms
from ..models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'primer_nombre',
            'segundo_nombre',
            'primer_apellido',
            'segundo_apellido',
            'email',
            'cedula',
            'telefono',
            'telefono_fijo',
            'direccion',
        ]
        widgets = {
            'primer_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el primer nombre'
            }),
            'segundo_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el segundo nombre (opcional)'
            }),
            'primer_apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el primer apellido'
            }),
            'segundo_apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el segundo apellido (opcional)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@correo.com'
            }),
            'cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número de cédula'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número de celular'
            }),
            'telefono_fijo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número fijo (opcional)'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese la dirección completa'
            }),
        }
        labels = {
            'primer_nombre': 'Primer Nombre',
            'segundo_nombre': 'Segundo Nombre',
            'primer_apellido': 'Primer Apellido',
            'segundo_apellido': 'Segundo Apellido',
            'email': 'Correo Electrónico',
            'cedula': 'Cédula',
            'telefono': 'Teléfono Celular',
            'telefono_fijo': 'Teléfono Fijo',
            'direccion': 'Dirección',
        }