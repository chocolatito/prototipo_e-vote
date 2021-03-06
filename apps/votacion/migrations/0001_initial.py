# Generated by Django 3.0 on 2021-02-27 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eleccion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
                ('candidato', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='eleccion.Candidato')),
            ],
            options={
                'verbose_name': 'Voto',
                'verbose_name_plural': 'Votos',
                'ordering': ['candidato'],
            },
        ),
        migrations.CreateModel(
            name='Urna',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
                ('urna_status', models.IntegerField(choices=[(0, 'Preparada'), (1, 'Esperando'), (2, 'En operacion'), (3, 'Concluida'), (4, 'Cerrada')], default=0)),
                ('eleccion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='eleccion.Eleccion')),
                ('votos', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='votacion.Voto')),
            ],
            options={
                'verbose_name': 'Urna',
                'verbose_name_plural': 'Urnas',
                'ordering': ['urna_status'],
            },
        ),
    ]
