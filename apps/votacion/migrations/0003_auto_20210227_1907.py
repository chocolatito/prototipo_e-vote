# Generated by Django 3.0 on 2021-02-27 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eleccion', '0001_initial'),
        ('votacion', '0002_voto_counting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voto',
            name='candidato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eleccion.Candidato'),
        ),
    ]
