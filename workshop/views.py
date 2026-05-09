from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import localdate
import requests as http_requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .models import CategoriAlimento, Alimento, RegistoDiario, Refeicao, RefeicaoAlimento, Objetivo
from .forms import CategoriAlimentoForm, AlimentoForm, RegistoDiarioForm, RefeicaoForm, RefeicaoAlimentoForm, ObjetivoForm, RegistoUtilizadorForm


def register(request):
    if request.method == 'POST':
        form = RegistoUtilizadorForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegistoUtilizadorForm()
    return render(request, 'workshop/register.html', {'form': form})


@login_required
def index(request):
    hoje = localdate()

    objetivo = Objetivo.objects.filter(utilizador=request.user).order_by('-data_inicio').first()

    calorias_hoje = 0.0
    proteina_hoje = 0.0
    hidratos_hoje = 0.0
    gordura_hoje  = 0.0

    refeicoes_hoje = []
    registo_hoje = RegistoDiario.objects.filter(utilizador=request.user, data=hoje).first()
    if registo_hoje:
        for refeicao in registo_hoje.refeicoes.all().order_by('hora'):
            cal_ref = 0.0
            for item in refeicao.itens.all():
                fator = item.quantidade_g / 100
                cal_ref       += item.alimento.calorias_por_100g * fator
                calorias_hoje += item.alimento.calorias_por_100g * fator
                proteina_hoje += item.alimento.proteina_g        * fator
                hidratos_hoje += item.alimento.hidratos_g        * fator
                gordura_hoje  += item.alimento.gordura_g         * fator
            refeicoes_hoje.append({'refeicao': refeicao, 'calorias': round(cal_ref, 0)})

    calorias_hoje = round(calorias_hoje, 1)
    proteina_hoje = round(proteina_hoje, 1)
    hidratos_hoje = round(hidratos_hoje, 1)
    gordura_hoje  = round(gordura_hoje,  1)

    def pct(valor, alvo):
        if alvo and alvo > 0:
            return min(round((valor / alvo) * 100, 1), 100)
        return 0

    context = {
        'num_categorias': CategoriAlimento.objects.filter(utilizador=request.user).count(),
        'num_alimentos':  Alimento.objects.filter(utilizador=request.user).count(),
        'num_registos':   RegistoDiario.objects.filter(utilizador=request.user).count(),
        'num_refeicoes':  Refeicao.objects.filter(registo__utilizador=request.user).count(),
        'objetivo':        objetivo,
        'calorias_hoje':   calorias_hoje,
        'proteina_hoje':   proteina_hoje,
        'hidratos_hoje':   hidratos_hoje,
        'gordura_hoje':    gordura_hoje,
        'calorias_restantes': round((objetivo.calorias_alvo - calorias_hoje), 1) if objetivo else 0,

        'pct_calorias': pct(calorias_hoje, objetivo.calorias_alvo     if objetivo else 0),
        'ring_offset':  round(565 - 565 * pct(calorias_hoje, objetivo.calorias_alvo if objetivo else 0) / 100, 1),
        'pct_proteina': pct(proteina_hoje, objetivo.proteina_alvo_g   if objetivo else 0),
        'pct_hidratos': pct(hidratos_hoje, objetivo.hidratos_alvo_g   if objetivo else 0),
        'pct_gordura':  pct(gordura_hoje,  objetivo.gordura_alvo_g    if objetivo else 0),

        'refeicoes_hoje': refeicoes_hoje,
    }
    return render(request, 'workshop/index.html', context)


# --- Categoria ---
class CategoriAlimentoListView(LoginRequiredMixin, ListView):
    model = CategoriAlimento
    template_name = 'workshop/categorialimento_list.html'
    context_object_name = 'categorias'

    def get_queryset(self):
        return CategoriAlimento.objects.filter(utilizador=self.request.user).annotate(
            num_alimentos_user=Count('alimentos', filter=Q(alimentos__utilizador=self.request.user))
        )

class CategoriAlimentoCreateView(LoginRequiredMixin, CreateView):
    model = CategoriAlimento
    form_class = CategoriAlimentoForm
    template_name = 'workshop/form_generic.html'
    success_url = reverse_lazy('categorias')

    def form_valid(self, form):
        form.instance.utilizador = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Adicionar categoria'
        ctx['voltar_url'] = reverse_lazy('categorias')
        return ctx

class CategoriAlimentoDeleteView(LoginRequiredMixin, DeleteView):
    model = CategoriAlimento
    template_name = 'workshop/delete_form.html'
    success_url = reverse_lazy('categorias')

    def get_queryset(self):
        return CategoriAlimento.objects.filter(utilizador=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['voltar_url'] = reverse_lazy('categorias')
        return ctx

class CategoriAlimentoUpdateView(LoginRequiredMixin, UpdateView):
    model = CategoriAlimento
    form_class = CategoriAlimentoForm
    template_name = 'workshop/form_generic.html'
    success_url = reverse_lazy('categorias')

    def get_queryset(self):
        return CategoriAlimento.objects.filter(utilizador=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar categoria'
        ctx['voltar_url'] = reverse_lazy('categorias')
        return ctx


# --- Alimento ---
class AlimentoListView(LoginRequiredMixin, ListView):
    model = Alimento
    template_name = 'workshop/alimento_list.html'
    context_object_name = 'alimentos'

    def get_queryset(self):
        return Alimento.objects.filter(utilizador=self.request.user)

class AlimentoCreateView(LoginRequiredMixin, CreateView):
    model = Alimento
    form_class = AlimentoForm
    template_name = 'workshop/form_generic.html'
    success_url = reverse_lazy('alimentos')

    def form_valid(self, form):
        form.instance.utilizador = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['categoria'].queryset = CategoriAlimento.objects.filter(utilizador=self.request.user)
        return form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Adicionar alimento'
        ctx['voltar_url'] = reverse_lazy('alimentos')
        return ctx

class AlimentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Alimento
    template_name = 'workshop/delete_form.html'
    success_url = reverse_lazy('alimentos')

    def get_queryset(self):
        return Alimento.objects.filter(utilizador=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['voltar_url'] = reverse_lazy('alimentos')
        return ctx

class AlimentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Alimento
    form_class = AlimentoForm
    template_name = 'workshop/form_generic.html'
    success_url = reverse_lazy('alimentos')

    def get_queryset(self):
        return Alimento.objects.filter(utilizador=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['categoria'].queryset = CategoriAlimento.objects.filter(utilizador=self.request.user)
        return form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar alimento'
        ctx['voltar_url'] = reverse_lazy('alimentos')
        return ctx


# --- Registo Diário ---
class RegistoDiarioListView(LoginRequiredMixin, ListView):
    model = RegistoDiario
    template_name = 'workshop/registodiario_list.html'
    context_object_name = 'registos'

    def get_queryset(self):
        return RegistoDiario.objects.filter(utilizador=self.request.user).order_by('-data')

class RegistoDiarioCreateView(LoginRequiredMixin, CreateView):
    model = RegistoDiario
    form_class = RegistoDiarioForm
    template_name = 'workshop/form_generic.html'
    success_url = reverse_lazy('registos')

    def form_valid(self, form):
        form.instance.utilizador = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Adicionar registo diário'
        ctx['voltar_url'] = reverse_lazy('registos')
        return ctx

class RegistoDiarioDeleteView(LoginRequiredMixin, DeleteView):
    model = RegistoDiario
    template_name = 'workshop/delete_form.html'
    success_url = reverse_lazy('registos')

    def get_queryset(self):
        return RegistoDiario.objects.filter(utilizador=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['voltar_url'] = reverse_lazy('registos')
        return ctx

class RegistoDiarioUpdateView(LoginRequiredMixin, UpdateView):
    model = RegistoDiario
    form_class = RegistoDiarioForm
    template_name = 'workshop/form_generic.html'
    success_url = reverse_lazy('registos')

    def get_queryset(self):
        return RegistoDiario.objects.filter(utilizador=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar registo diário'
        ctx['voltar_url'] = reverse_lazy('registos')
        return ctx


# --- Refeição ---
class RefeicaoListView(LoginRequiredMixin, ListView):
    model = Refeicao
    template_name = 'workshop/refeicao_list.html'
    context_object_name = 'refeicoes'

    def get_queryset(self):
        return Refeicao.objects.filter(registo__utilizador=self.request.user).order_by('-registo__data')

class RefeicaoCreateView(LoginRequiredMixin, CreateView):
    model = Refeicao
    form_class = RefeicaoForm
    template_name = 'workshop/form_generic.html'
    success_url = reverse_lazy('refeicoes')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['registo'].queryset = RegistoDiario.objects.filter(utilizador=self.request.user)
        return form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Adicionar refeição'
        ctx['voltar_url'] = reverse_lazy('refeicoes')
        return ctx

class RefeicaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Refeicao
    template_name = 'workshop/delete_form.html'
    success_url = reverse_lazy('refeicoes')

    def get_queryset(self):
        return Refeicao.objects.filter(registo__utilizador=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['voltar_url'] = reverse_lazy('refeicoes')
        return ctx

class RefeicaoUpdateView(LoginRequiredMixin, UpdateView):
    model = Refeicao
    form_class = RefeicaoForm
    template_name = 'workshop/form_generic.html'
    success_url = reverse_lazy('refeicoes')

    def get_queryset(self):
        return Refeicao.objects.filter(registo__utilizador=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['registo'].queryset = RegistoDiario.objects.filter(utilizador=self.request.user)
        return form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar refeição'
        ctx['voltar_url'] = reverse_lazy('refeicoes')
        return ctx


class RefeicaoAlimentoCreateView(LoginRequiredMixin, CreateView):
    model = RefeicaoAlimento
    form_class = RefeicaoAlimentoForm
    template_name = 'workshop/form_generic.html'
    success_url = reverse_lazy('refeicoes')

    def dispatch(self, request, *args, **kwargs):
        self.refeicao = Refeicao.objects.get(pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['alimento'].queryset = Alimento.objects.filter(utilizador=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.refeicao = self.refeicao
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = f"Adicionar alimento - {self.refeicao.get_tipo_display()}"
        ctx['voltar_url'] = reverse_lazy('refeicoes')
        return ctx


class RefeicaoAlimentoDeleteView(LoginRequiredMixin, DeleteView):
    model = RefeicaoAlimento
    template_name = 'workshop/delete_form.html'
    success_url = reverse_lazy('refeicoes')

    def get_queryset(self):
        return RefeicaoAlimento.objects.filter(refeicao__registo__utilizador=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['voltar_url'] = reverse_lazy('refeicoes')
        return ctx


# --- Objetivo ---
class ObjetivoListView(LoginRequiredMixin, ListView):
    model = Objetivo
    template_name = 'workshop/objetivo_list.html'

    def get_queryset(self):
        return Objetivo.objects.filter(utilizador=self.request.user).order_by('-data_inicio')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['objetivo'] = self.get_queryset().first()
        return ctx

class ObjetivoCreateView(LoginRequiredMixin, CreateView):
    model = Objetivo
    form_class = ObjetivoForm
    template_name = 'workshop/form_generic.html'
    success_url = reverse_lazy('objetivos')

    def dispatch(self, request, *args, **kwargs):
        existing = Objetivo.objects.filter(utilizador=request.user).first()
        if existing:
            return redirect('objetivo_editar', pk=existing.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.utilizador = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Definir objetivo'
        ctx['voltar_url'] = reverse_lazy('objetivos')
        return ctx

class ObjetivoDeleteView(LoginRequiredMixin, DeleteView):
    model = Objetivo
    template_name = 'workshop/delete_form.html'
    success_url = reverse_lazy('objetivos')

    def get_queryset(self):
        return Objetivo.objects.filter(utilizador=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['voltar_url'] = reverse_lazy('objetivos')
        return ctx

class ObjetivoUpdateView(LoginRequiredMixin, UpdateView):
    model = Objetivo
    form_class = ObjetivoForm
    template_name = 'workshop/form_generic.html'
    success_url = reverse_lazy('objetivos')

    def get_queryset(self):
        return Objetivo.objects.filter(utilizador=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar objetivo'
        ctx['voltar_url'] = reverse_lazy('objetivos')
        return ctx


# --- Open Food Facts ---
PAGE_SIZE = 20

@login_required
def off_search(request):
    query = request.GET.get('q', '').strip()
    page  = max(1, int(request.GET.get('page', 1) or 1))
    results = []
    error = None
    total = 0

    if query:
        try:
            session = http_requests.Session()
            retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
            session.mount('https://', HTTPAdapter(max_retries=retries))

            resp = session.get(
                'https://world.openfoodfacts.org/cgi/search.pl',
                params={
                    'search_terms': query,
                    'search_simple': 1,
                    'action': 'process',
                    'json': 1,
                    'page': page,
                    'page_size': PAGE_SIZE,
                    'fields': 'product_name,nutriments,brands,image_front_small_url',
                },
                timeout=15,
                headers={'User-Agent': 'CalTrack - Educational Project - contact@example.com'},
            )
            resp.raise_for_status()
            data = resp.json()
            total = int(data.get('count') or 0)
            for p in data.get('products', []):
                name = p.get('product_name', '').strip()
                if not name:
                    continue
                n = p.get('nutriments', {})
                results.append({
                    'nome': name,
                    'marca': p.get('brands', '') or '',
                    'imagem': p.get('image_front_small_url', '') or '',
                    'calorias': round(float(n.get('energy-kcal_100g') or 0), 1),
                    'proteina': round(float(n.get('proteins_100g') or 0), 1),
                    'hidratos': round(float(n.get('carbohydrates_100g') or 0), 1),
                    'gordura':  round(float(n.get('fat_100g') or 0), 1),
                })
        except Exception:
            error = 'Não foi possível contactar o Open Food Facts. Verifica a tua ligação e tenta novamente.'

    import math
    total_pages = math.ceil(total / PAGE_SIZE) if total else 0

    return render(request, 'workshop/off_search.html', {
        'query': query,
        'results': results,
        'error': error,
        'page': page,
        'total': total,
        'total_pages': total_pages,
        'prev_page': page - 1 if page > 1 else None,
        'next_page': page + 1 if page < total_pages else None,
    })


@login_required
def off_importar(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        if nome:
            alimento = Alimento.objects.create(
                nome=nome,
                utilizador=request.user,
                calorias_por_100g=float(request.POST.get('calorias') or 0),
                proteina_g=float(request.POST.get('proteina') or 0),
                hidratos_g=float(request.POST.get('hidratos') or 0),
                gordura_g=float(request.POST.get('gordura') or 0),
            )
            imagem_url = request.POST.get('imagem_url', '').strip()
            if imagem_url:
                try:
                    img = http_requests.get(imagem_url, timeout=8)
                    if img.status_code == 200:
                        ext = imagem_url.split('.')[-1].split('?')[0][:4] or 'jpg'
                        alimento.imagem.save(f"off_{alimento.id}.{ext}", ContentFile(img.content), save=True)
                except Exception:
                    pass
    return redirect('alimentos')
