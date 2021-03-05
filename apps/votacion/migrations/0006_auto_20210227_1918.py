# Generated by Django 3.0 on 2021-02-27 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votacion', '0005_auto_20210227_1915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='urna',
            name='votos',
        ),
        migrations.AddField(
            model_name='voto',
            name='urna',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='votacion.Urna'),
        ),
    ]