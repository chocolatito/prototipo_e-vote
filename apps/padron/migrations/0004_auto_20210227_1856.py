# Generated by Django 3.0 on 2021-02-27 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('padron', '0003_group_membership_person'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('person', 'group')},
        ),
        migrations.AlterUniqueTogether(
            name='padronelector',
            unique_together={('padron', 'elector')},
        ),
    ]
