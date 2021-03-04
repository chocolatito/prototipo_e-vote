# from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
#
from django.utils.decorators import method_decorator
#
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
#
from .models import Voto, Urna
from ..eleccion.models import Candidato, Eleccion
from ..padron.models import PadronElector
# Create your views here.


# decorators = [login_required, group_required('administracion',)]
decorators = [login_required(login_url='usuarios:login'), ]


@method_decorator(decorators, name='dispatch')
class DisabledUrna(TemplateView):
    template_name = "votacion/urna.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = Urna.objects.get(pk=kwargs['pk'])
        if self.object.urna_status == 2:
            return redirect('votacion:enabled-urna', pk=self.object.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(f'----->>>{kwargs}\n\n')
        context['object'] = self.object
        return context


class EnabledUrna(TemplateView):
    template_name = "votacion/urna.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = Urna.objects.get(pk=kwargs['pk'])
        if self.object.urna_status == 2:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('votacion:disabled-urna', pk=self.object.pk)

    def post(self, request, *args, **kwargs):
        return redirect('votacion:confirmar',
                        pk=self.object.pk, candidato=request.POST['button'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs)
        context['object'] = self.object
        context['candidatos'] = self.object.eleccion.candidato_set.all().order_by('?')
        return context


class Confirmar(TemplateView):
    template_name = "votacion/confirmar.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = Urna.objects.get(pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST['button'] == "0":
            print("CANCELADO\n")
            return redirect('votacion:enabled-urna', pk=self.object.pk)
        else:
            print("CONFIRMADO\n")
            candidato = Candidato.objects.get(pk=request.POST['button'])
            Voto.objects.create(candidato=candidato, urna=self.object)
            self.object.urna_status = 3
            self.object.save()
            return redirect('votacion:disabled-urna', pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['candidato'] = kwargs['candidato']
        return context


# ____________________________
@method_decorator(decorators, name='dispatch')
class UrnaListView(ListView):
    model = Urna
    template_name = "eleccion/urna_list.html"

    def get_queryset(self):
        print(self.kwargs)
        self.eleccion = get_object_or_404(Eleccion, slug=self.kwargs['slug'])
        print(Urna.objects.filter(eleccion=self.eleccion))
        return Urna.objects.filter(eleccion=self.eleccion)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Urnas"
        context['page'] = "Listado de Urnas"
        context['eleccion'] = self.eleccion
        #
        return context


@method_decorator(decorators, name='dispatch')
class UrnaDetailView(DetailView):
    model = Urna
    template_name = "votacion/urna_detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Urna, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        elector = get_object_or_404(PadronElector, pk=request.POST['button'])
        if elector.transaction_status == 0:
            elector.transaction_status = 1
            elector.save()
            return redirect('votacion:urna-enabled-elector',
                            slug=kwargs['slug'],
                            pk=self.object.pk,
                            elector_pk=elector.pk)
        else:
            return redirect('index:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Urna"
        context['object'] = self.object
        context['padron'] = self.object.eleccion.padron
        context['slug'] = self.object.eleccion.slug
        context['thead'] = ['DNI', 'Nombre/s', 'Apellido/s', 'Condición']
        return context


@method_decorator(decorators, name='dispatch')
class UrnaEnebledElectorView(TemplateView):
    template_name = "votacion/urna_enabled_elector.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(PadronElector, pk=kwargs['elector_pk'])
        self.urna = get_object_or_404(Urna, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.object.transaction_status == 1:
            self.object.transaction_status = 2
            self.object.save()
            self.urna.urna_status = 2
            self.urna.save()
            return redirect('votacion:urna-enabled-elector',
                            slug=kwargs['slug'],
                            pk=kwargs['pk'],
                            elector_pk=kwargs['elector_pk'])
        elif self.object.transaction_status == 2:
            self.object.transaction_status = 3
            self.object.save()
            self.urna.urna_status = 1
            self.urna.save()
            return redirect('votacion:urna-detail',
                            slug=kwargs['slug'],
                            pk=kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Urna"
        context['object'] = self.object
        context['thead'] = ['DNI', 'Nombre/s', 'Apellido/s', 'Condición']
        return context
