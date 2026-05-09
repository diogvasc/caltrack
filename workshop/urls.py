from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Categorias
    path('categorias/', views.CategoriAlimentoListView.as_view(), name='categorias'),
    path('categorias/adicionar/', views.CategoriAlimentoCreateView.as_view(), name='categoria_criar'),
    path('categorias/<int:pk>/editar/', views.CategoriAlimentoUpdateView.as_view(), name='categoria_editar'),
    path('categorias/<int:pk>/apagar/', views.CategoriAlimentoDeleteView.as_view(), name='categoria_apagar'),

    # Alimentos
    path('alimentos/', views.AlimentoListView.as_view(), name='alimentos'),
    path('alimentos/adicionar/', views.AlimentoCreateView.as_view(), name='alimento_criar'),
    path('alimentos/importar/', views.off_search, name='off_search'),
    path('alimentos/importar/confirmar/', views.off_importar, name='off_importar'),
    path('alimentos/<int:pk>/editar/', views.AlimentoUpdateView.as_view(), name='alimento_editar'),
    path('alimentos/<int:pk>/apagar/', views.AlimentoDeleteView.as_view(), name='alimento_apagar'),

    # Registos diários
    path('registos/', views.RegistoDiarioListView.as_view(), name='registos'),
    path('registos/adicionar/', views.RegistoDiarioCreateView.as_view(), name='registo_criar'),
    path('registos/<int:pk>/editar/', views.RegistoDiarioUpdateView.as_view(), name='registo_editar'),
    path('registos/<int:pk>/apagar/', views.RegistoDiarioDeleteView.as_view(), name='registo_apagar'),

    # Refeições
    path('refeicoes/', views.RefeicaoListView.as_view(), name='refeicoes'),
    path('refeicoes/adicionar/', views.RefeicaoCreateView.as_view(), name='refeicao_criar'),
    path('refeicoes/<int:pk>/editar/', views.RefeicaoUpdateView.as_view(), name='refeicao_editar'),
    path('refeicoes/<int:pk>/alimentos/adicionar/', views.RefeicaoAlimentoCreateView.as_view(), name='refeicao_alimento_criar'),
    path('refeicoes/itens/<int:pk>/remover/', views.RefeicaoAlimentoDeleteView.as_view(), name='refeicao_item_apagar'),
    path('refeicoes/<int:pk>/apagar/', views.RefeicaoDeleteView.as_view(), name='refeicao_apagar'),

    # Objetivos
    path('objetivos/', views.ObjetivoListView.as_view(), name='objetivos'),
    path('objetivos/adicionar/', views.ObjetivoCreateView.as_view(), name='objetivo_criar'),
    path('objetivos/<int:pk>/editar/', views.ObjetivoUpdateView.as_view(), name='objetivo_editar'),
    path('objetivos/<int:pk>/apagar/', views.ObjetivoDeleteView.as_view(), name='objetivo_apagar'),
]