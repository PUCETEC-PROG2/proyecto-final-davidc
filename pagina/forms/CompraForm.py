from django import forms
from ..models import Compra, Cliente, Propiedad
from django.utils.html import format_html

class PropiedadTableWidget(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        output = ['<table class="table">']
        output += ['<thead><tr><th>ID</th><th>Producto</th><th>Categoría</th><th>Precio</th><th>Seleccionar</th></tr></thead>']
        output += ['<tbody>']
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, {'name': name})
        str_values = {str(v) for v in value} if value else set()  # Verifica si value es None
        for i, (option_value, option_label) in enumerate(self.choices):
            # Obtener la instancia de Propiedad
            propiedad_id = option_value.value  # Obtener el ID de la propiedad
            propiedad = Propiedad.objects.get(pk=propiedad_id)
            output += ['<tr>']
            output += ['<td>{}</td>'.format(propiedad.id)]
            output += ['<td>{}</td>'.format(propiedad.nombre)]
            output += ['<td>{}</td>'.format(propiedad.categoria)]
            output += ['<td>{}</td>'.format(propiedad.precio)]
            cb_id = '%s_%s' % (final_attrs['id'], i) if final_attrs.get('id') else ''
            
            # Construir el checkbox
            cb = forms.CheckboxInput(
                attrs={'id': cb_id, 'value': propiedad_id, 'data-precio': propiedad.precio},
                check_test=lambda value: str(value) in str_values
            )
            rendered_cb = cb.render(name, propiedad_id)
            output += ['<td>{}</td>'.format(rendered_cb)]
            output += ['</tr>']
        output += ['</tbody></table>']
        return format_html('\n'.join(output))

class CompraForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    propiedades = forms.ModelMultipleChoiceField(
        queryset=Propiedad.objects.filter(estado='disponible'),
        widget=PropiedadTableWidget(attrs={'class': 'form-check-input'})
    )
    fecha_compra = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control datepicker'})
    )

    class Meta:
        model = Compra
        fields = ['cliente', 'propiedades', 'fecha_compra']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['propiedades'].label = "Seleccione las propiedades:" 

