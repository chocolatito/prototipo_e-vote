# Generated by Django 3.0 on 2021-02-27 14:51

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Elector',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
                ('dni', models.IntegerField(default=0, verbose_name='DNI')),
                ('names', models.CharField(max_length=100, verbose_name='Nombre/s')),
                ('surnames', models.CharField(max_length=100, verbose_name='Apellido/s')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Elector',
                'verbose_name_plural': 'Electores',
                'ordering': ['surnames', 'names'],
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Padron',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('date', models.DateField(default=datetime.date.today)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Padron',
                'verbose_name_plural': 'Padrones',
                'ordering': ['date', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='PadronElector',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
                ('transaction_status', models.IntegerField(choices=[(0, 'Ausente'), (1, 'Identificado'), (2, 'Votando'), (3, 'Completado'), (4, 'Suspendido')], default=0)),
                ('transaction_datetime', models.DateTimeField(blank=True, editable=False, null=True)),
                ('transaction_code', models.UUIDField(blank=True, editable=False, null=True)),
                ('elector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='padron.Elector')),
                ('padron', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='padron.Padron')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='padron',
            name='electores',
            field=models.ManyToManyField(through='padron.PadronElector', to='padron.Elector'),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='padron.Group')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='padron.Person')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(through='padron.Membership', to='padron.Person'),
        ),
    ]
