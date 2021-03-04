from django.db import models
from django.urls import reverse
from ..BaseModel import Base
from ..eleccion.models import Eleccion, Candidato

# Create your models here.

URNA_STATUS = [(0, 'Preparada'),
               (1, 'Esperando'), (2, 'En operacion'), (3, 'Concluida'),
               (4, 'Cerrada'), ]


class Voto(Base):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    counting = models.BooleanField(default=False)
    urna = models.ForeignKey('Urna', on_delete=models.CASCADE)

    class Meta:
        ordering = ['candidato']
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'

    def __str__(self):
        return f'{self.id}-{self.candidato}'


class Urna(Base):
    urna_status = models.IntegerField(choices=URNA_STATUS, default=0)
    # eleccion = models.OneToOneField(Eleccion, on_delete=models.CASCADE)
    eleccion = models.ForeignKey(Eleccion, on_delete=models.CASCADE)

    class Meta:
        ordering = ['urna_status']
        verbose_name = 'Urna'
        verbose_name_plural = 'Urnas'

    def get_absolute_url(self):
        return reverse('votacion:urna-detail', args=[str(self.eleccion.slug), str(self.id)])

    def __str__(self):
        return f'{self.eleccion}-{self.get_urna_status_display()}'
