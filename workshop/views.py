from django.views.generic import ListView, CreateView, DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import CategoriAlimento, Alimento, RegistoDiario, Refeicao, RefeicaoAlimento, Objetivo
from .forms import CategoriAlimentoForm, AlimentoForm, RegistoDiarioForm, RefeicaoForm, ObjetivoForm


def index(request):
    context = {
        'num_categorias': CategoriAlimento.objects.count(),
        'num_alimentos': Alimento.objects.count(),
        'num_registos': RegistoDiario.objects.count(),
        'num_refeicoes': Refeicao.objects.count(),
        'num_objetivos': Objetivo.objects.count(),
    }
    return render(request, 'workshop/index.html', context)


# --- Categoria ---
class CategoriAlimentoListView(ListView):
    model = CategoriAlimento
    template_name = 'workshop/categorialimento_list.html'
    context_object_name = 'categorias'

class CategoriAlimentoCreateView(CreateView):
    model = CategoriAlimento
    form_class = CategoriAlimentoForm
    template_name = 'workshop/form_generic.html'
    success_url = reverse_lazy('categorias')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Adicionar categoria'
        ctx['voltar_url'] = reverse_lazy('categorias')
        return ctx

class CategoriAlimentoDeleteView(DeleteView):
    model = CategoriAlimento
    template_name = 'workshop/delete_form.html'
    success_url = reverse_lazy('categorias')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['voltar_url'] = reverse_lazy('categorias')
        return ctx


# --- Alimento ---
class AlimentoListView(ListView):
    model = Alimento
    template_name = 'workshop/alimento_list.html'
    context_object_name = 'alimentos'

class AlimentoCreateView(CreateView):
    model = Alimento
    form_class = AlimentoForm
    template_name = 'workshop/form_generic.html'
    success_url = reverse_lazy('alimentos')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Adicionar alimento'
        ctx['voltar_url'] = reverse_lazy('alimentos')
        return ctx

class AlimentoDeleteView(DeleteView):
    model = Alimento
    template_name = 'workshop/delete_form.html'
    success_url = reverse_lazy('alimentos')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['voltar_url'] = reverse_lazy('alimentos')
        return ctx


# --- Registo Diário ---
class RegistoDiarioListView(ListView):
    model = RegistoDiario
    template_name = 'workshop/registodiario_list.html'
    context_object_name = 'registos'

class RegistoDiarioCreateView(CreateView):
    model = RegistoDiario
    form_class = RegistoDiarioForm
    template_name = 'workshop/form_generic.html'
    success_url = reverse_lazy('registos')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Adicionar registo diário'
        ctx['voltar_url'] = reverse_lazy('registos')
        return ctx

class RegistoDiarioDeleteView(DeleteView):
    model = RegistoDiario
    template_name = 'workshop/delete_form.html'
    success_url = reverse_lazy('registos')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['voltar_url'] = reverse_lazy('registos')
        return ctx


# --- Refeição ---
class RefeicaoListView(ListView):
    model = Refeicao
    template_name = 'workshop/refeicao_list.html'
    context_object_name = 'refeicoes'

class RefeicaoCreateView(CreateView):
    model = Refeicao
    form_class = RefeicaoForm
    template_name = 'workshop/form_generic.html'
    success_url = reverse_lazy('refeicoes')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Adicionar refeição'
        ctx['voltar_url'] = reverse_lazy('refeicoes')
        return ctx

class RefeicaoDeleteView(DeleteView):
    model = Refeicao
    template_name = 'workshop/delete_form.html'
    success_url = reverse_lazy('refeicoes')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['voltar_url'] = reverse_lazy('refeicoes')
        return ctx


# --- Objetivo ---
class ObjetivoListView(ListView):
    model = Objetivo
    template_name = 'workshop/objetivo_list.html'
    context_object_name = 'objetivos'

class ObjetivoCreateView(CreateView):
    model = Objetivo
    form_class = ObjetivoForm
    template_name = 'workshop/form_generic.html'
    success_url = reverse_lazy('objetivos')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Adicionar objetivo'
        ctx['voltar_url'] = reverse_lazy('objetivos')
        return ctx

class ObjetivoDeleteView(DeleteView):
    model = Objetivo
    template_name = 'workshop/delete_form.html'
    success_url = reverse_lazy('objetivos')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['voltar_url'] = reverse_lazy('objetivos')
        return ctx