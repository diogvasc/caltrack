from django.views.generic import ListView, CreateView, DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import CategoriAlimento, Alimento, RegistoDiario, Refeicao, RefeicaoAlimento, Objetivo
from .forms import AlimentoForm


def index(request):
    context = {
        'num_categorias': CategoriAlimento.objects.count(),
        'num_alimentos': Alimento.objects.count(),
        'num_registos': RegistoDiario.objects.count(),
        'num_refeicoes': Refeicao.objects.count(),
        'num_objetivos': Objetivo.objects.count(),
    }
    return render(request, 'workshop/index.html', context)


class CategoriAlimentoListView(ListView):
    model = CategoriAlimento
    template_name = 'workshop/categorialimento_list.html'
    context_object_name = 'categorias'


class AlimentoListView(ListView):
    model = Alimento
    template_name = 'workshop/alimento_list.html'
    context_object_name = 'alimentos'


class AlimentoCreateView(CreateView):
    model = Alimento
    form_class = AlimentoForm
    template_name = 'workshop/alimento_form.html'
    success_url = reverse_lazy('alimentos')


class AlimentoDeleteView(DeleteView):
    model = Alimento
    template_name = 'workshop/alimento_confirm_delete.html'
    success_url = reverse_lazy('alimentos')


class RegistoDiarioListView(ListView):
    model = RegistoDiario
    template_name = 'workshop/registodiario_list.html'
    context_object_name = 'registos'


class RefeicaoListView(ListView):
    model = Refeicao
    template_name = 'workshop/refeicao_list.html'
    context_object_name = 'refeicoes'


class ObjetivoListView(ListView):
    model = Objetivo
    template_name = 'workshop/objetivo_list.html'
    context_object_name = 'objetivos'