# Generated by Django 3.0 on 2021-03-02 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eleccion', '0001_initial'),
        ('votacion', '0007_auto_20210227_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urna',
            name='eleccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eleccion.Eleccion'),
        ),
    ]
