from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categorias/', views.CategoriAlimentoListView.as_view(), name='categorias'),
    path('alimentos/', views.AlimentoListView.as_view(), name='alimentos'),
    path('registos/', views.RegistoDiarioListView.as_view(), name='registos'),
    path('refeicoes/', views.RefeicaoListView.as_view(), name='refeicoes'),
    path('objetivos/', views.ObjetivoListView.as_view(), name='objetivos'),
]