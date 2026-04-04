from django import forms
from .models import Alimento, CategoriAlimento, RegistoDiario, Refeicao, Objetivo


class CategoriAlimentoForm(forms.ModelForm):
    class Meta:
        model = CategoriAlimento
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Frutas'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descrição opcional...', 'rows': 3}),
        }


class AlimentoForm(forms.ModelForm):
    class Meta:
        model = Alimento
        fields = ['nome', 'categoria', 'calorias_por_100g', 'proteina_g', 'hidratos_g', 'gordura_g', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Frango grelhado'}),
            'calorias_por_100g': forms.NumberInput(attrs={'placeholder': '0.0', 'step': '0.1'}),
            'proteina_g': forms.NumberInput(attrs={'placeholder': '0.0', 'step': '0.1'}),
            'hidratos_g': forms.NumberInput(attrs={'placeholder': '0.0', 'step': '0.1'}),
            'gordura_g': forms.NumberInput(attrs={'placeholder': '0.0', 'step': '0.1'}),
        }


class RegistoDiarioForm(forms.ModelForm):
    class Meta:
        model = RegistoDiario
        fields = ['utilizador', 'data', 'notas', 'agua_ml']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'notas': forms.Textarea(attrs={'placeholder': 'Notas do dia...', 'rows': 3}),
            'agua_ml': forms.NumberInput(attrs={'placeholder': '0', 'step': '50'}),
        }


class RefeicaoForm(forms.ModelForm):
    class Meta:
        model = Refeicao
        fields = ['registo', 'tipo', 'hora']
        widgets = {
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }


class ObjetivoForm(forms.ModelForm):
    class Meta:
        model = Objetivo
        fields = ['utilizador', 'calorias_alvo', 'proteina_alvo_g', 'hidratos_alvo_g', 'gordura_alvo_g', 'data_inicio', 'data_fim']
        widgets = {
            'calorias_alvo': forms.NumberInput(attrs={'placeholder': '0.0', 'step': '0.1'}),
            'proteina_alvo_g': forms.NumberInput(attrs={'placeholder': '0.0', 'step': '0.1'}),
            'hidratos_alvo_g': forms.NumberInput(attrs={'placeholder': '0.0', 'step': '0.1'}),
            'gordura_alvo_g': forms.NumberInput(attrs={'placeholder': '0.0', 'step': '0.1'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }