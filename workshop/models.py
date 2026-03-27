from django.db import models
from django.contrib.auth.models import User


class CategoriAlimento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome


class Alimento(models.Model):
    nome = models.CharField(max_length=200)
    calorias_por_100g = models.FloatField()
    proteina_g = models.FloatField(default=0.0)
    hidratos_g = models.FloatField(default=0.0)
    gordura_g = models.FloatField(default=0.0)
    categoria = models.ForeignKey(CategoriAlimento, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='alimentos')
    imagem = models.ImageField(upload_to='alimentos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.calorias_por_100g} kcal/100g)"


class RegistoDiario(models.Model):
    utilizador = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='registos')
    data = models.DateField()
    notas = models.TextField(blank=True)
    agua_ml = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.utilizador.username} – {self.data}"


class Refeicao(models.Model):
    TIPO_CHOICES = [
        ('pequeno_almoco', 'Pequeno-almoço'),
        ('almoco', 'Almoço'),
        ('jantar', 'Jantar'),
        ('lanche', 'Lanche'),
        ('outro', 'Outro'),
    ]

    registo = models.ForeignKey(RegistoDiario, on_delete=models.CASCADE,
        related_name='refeicoes')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    hora = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()} – {self.registo.data}"


class RefeicaoAlimento(models.Model):
    refeicao = models.ForeignKey(Refeicao, on_delete=models.CASCADE,
        related_name='itens')
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE,
        related_name='itens')
    quantidade_g = models.FloatField()

    def __str__(self):
        return f"{self.quantidade_g}g de {self.alimento.nome}"


class Objetivo(models.Model):
    utilizador = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='objetivos')
    calorias_alvo = models.FloatField()
    proteina_alvo_g = models.FloatField(default=0.0)
    hidratos_alvo_g = models.FloatField(default=0.0)
    gordura_alvo_g = models.FloatField(default=0.0)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.utilizador.username} – {self.calorias_alvo} kcal/dia"