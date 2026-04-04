from django import forms
from .models import Alimento, CategoriAlimento


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