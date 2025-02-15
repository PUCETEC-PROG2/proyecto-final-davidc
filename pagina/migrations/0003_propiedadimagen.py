# Generated by Django 5.1.5 on 2025-02-14 01:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0002_propiedad_numero_particular'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropiedadImagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='propiedad_imagenes/')),
                ('propiedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='pagina.propiedad')),
            ],
        ),
    ]
