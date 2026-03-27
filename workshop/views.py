from django.views.generic import ListView
from django.shortcuts import render
from .models import CategoriAlimento, Alimento, RegistoDiario, Refeicao, RefeicaoAlimento, Objetivo


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