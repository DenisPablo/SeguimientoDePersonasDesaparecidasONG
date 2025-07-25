# Generated by Django 5.2.4 on 2025-07-23 00:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('estado', models.BooleanField(default=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Imagen',
                'verbose_name_plural': 'Imágenes',
            },
        ),
        migrations.CreateModel(
            name='PersonaDesaparecida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('nro_documento', models.CharField(blank=True, max_length=20, null=True)),
                ('genero', models.CharField(blank=True, max_length=10, null=True)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('estado_salud', models.CharField(blank=True, max_length=50, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('nro_calzado', models.IntegerField(blank=True, null=True)),
                ('altura', models.FloatField(blank=True, null=True)),
                ('peso', models.FloatField(blank=True, null=True)),
                ('fecha_desaparicion', models.DateTimeField(blank=True, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('imagen_perfil', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personas_desaparecidas', to='registro.imagen')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personas_desaparecidas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Persona desaparecida',
                'verbose_name_plural': 'Personas desaparecidas',
            },
        ),
        migrations.CreateModel(
            name='Pista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pistas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pista',
                'verbose_name_plural': 'Pistas',
            },
        ),
        migrations.CreateModel(
            name='ImagenPista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('imagen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes_pista', to='registro.imagen')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes_pista', to=settings.AUTH_USER_MODEL)),
                ('pista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='registro.pista')),
            ],
            options={
                'verbose_name': 'Imagen de pista',
                'verbose_name_plural': 'Imágenes de pista',
            },
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('estado', models.BooleanField(default=True)),
                ('persona_desaparecida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportes', to='registro.personadesaparecida')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reporte',
                'verbose_name_plural': 'Reportes',
            },
        ),
        migrations.AddField(
            model_name='pista',
            name='reporte',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pistas', to='registro.reporte'),
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ubicaciones', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ubicación',
                'verbose_name_plural': 'Ubicaciones',
            },
        ),
        migrations.CreateModel(
            name='UbicacionPista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('pista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ubicaciones', to='registro.pista')),
                ('ubicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ubicaciones_pista', to='registro.ubicacion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ubicaciones_pista', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ubicación de pista',
                'verbose_name_plural': 'Ubicaciones de pista',
            },
        ),
    ]
