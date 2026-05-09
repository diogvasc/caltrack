from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Alimento, CategoriAlimento, RegistoDiario, Refeicao, RefeicaoAlimento, Objetivo


class RegistoUtilizadorForm(UserCreationForm):
    username = forms.CharField(
        label='Nome de utilizador',
        widget=forms.TextInput(attrs={'placeholder': 'Ex: joao123'}),
    )
    password1 = forms.CharField(
        label='Palavra-passe',
        widget=forms.PasswordInput(),
        help_text='Mínimo 8 caracteres. Não pode ser só números.',
    )
    password2 = forms.CharField(
        label='Confirmar palavra-passe',
        widget=forms.PasswordInput(),
        help_text='Introduz a mesma palavra-passe para confirmação.',
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


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
        fields = ['data', 'notas', 'agua_ml']
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


class RefeicaoAlimentoForm(forms.ModelForm):
    class Meta:
        model = RefeicaoAlimento
        fields = ['alimento', 'quantidade_g']
        widgets = {
            'quantidade_g': forms.NumberInput(attrs={'placeholder': '0.0', 'step': '0.1'}),
        }


class ObjetivoForm(forms.ModelForm):
    class Meta:
        model = Objetivo
        fields = ['calorias_alvo', 'proteina_alvo_g', 'hidratos_alvo_g', 'gordura_alvo_g', 'data_inicio', 'data_fim']
        widgets = {
            'calorias_alvo': forms.NumberInput(attrs={'placeholder': '0.0', 'step': '0.1'}),
            'proteina_alvo_g': forms.NumberInput(attrs={'placeholder': '0.0', 'step': '0.1'}),
            'hidratos_alvo_g': forms.NumberInput(attrs={'placeholder': '0.0', 'step': '0.1'}),
            'gordura_alvo_g': forms.NumberInput(attrs={'placeholder': '0.0', 'step': '0.1'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }