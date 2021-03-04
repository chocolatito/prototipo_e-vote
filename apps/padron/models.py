import datetime

from django.db import models
from django.urls import reverse
# # #
from django.utils.text import slugify
# # # #
from django.db.models.signals import post_save
from django.contrib.auth.models import User
#
from ..BaseModel import Base
# _________________________________________
# https://docs.djangoproject.com/en/3.1/topics/db/models/#extra-fields-on-many-to-many-relationships


class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')
    dni = models.IntegerField(null=False, blank=False,
                              default=0, verbose_name="DNI")

    class Meta:
        unique_together = [['person', 'group']]


class Elector(Base):
    dni = models.IntegerField(null=False, blank=False,
                              default=0, verbose_name="DNI")
    names = models.CharField(verbose_name="Nombre/s",
                             max_length=100, null=False, blank=False)
    surnames = models.CharField(verbose_name="Apellido/s",
                                max_length=100, null=False, blank=False)
    user = models.ForeignKey(User, verbose_name="Usuario",
                             on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['surnames', 'names']
        verbose_name = "Elector"
        verbose_name_plural = "Electores"

    def get_absolute_url(self):
        pass

    def get_field_values_votacion(self):
        return [self.dni, self.names, self.surnames]

    def __str__(self):
        return "{} - {}, {}".format(self.dni, self.names, self.surnames)


class Padron(Base):
    title = models.CharField(max_length=100, null=False, blank=True)
    date = models.DateField(default=datetime.date.today)
    slug = models.SlugField(null=False, blank=False, unique=True)
    # Relationships
    electores = models.ManyToManyField(Elector, through='PadronElector')

    class Meta:
        ordering = ['date', 'id']
        verbose_name = "Padron"
        verbose_name_plural = "Padrones"

    def get_absolute_url(self):
        pass

    def __str__(self):
        return "{}/{} {}".format(self.date, self.id, self.title)


PADRONELECTOR_STATUS = [(0, "Ausente"),
                        (1, "Identificado"), (2, "Votando"), (3, "Completado"),
                        (4, "Suspendido"), ]


class PadronElector(Base):
    padron = models.ForeignKey(Padron, on_delete=models.CASCADE)
    elector = models.ForeignKey(Elector, on_delete=models.CASCADE)
    transaction_status = models.IntegerField(choices=PADRONELECTOR_STATUS, default=0)
    transaction_datetime = models.DateTimeField(null=True, blank=True, editable=False)
    transaction_code = models.UUIDField(null=True, blank=True, editable=False)

    class Meta:
        unique_together = [['padron', 'elector']]


#
# PRE/POST SAVE


def set_slug_Padron(sender, instance, *args, **kwargs):
    if instance.id and instance.date and not instance.slug:
        instance.slug = slugify(f'{instance.date}__{instance.id}')
        instance.save()


post_save.connect(set_slug_Padron, sender=Padron)
