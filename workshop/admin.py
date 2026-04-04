from django.contrib import admin
from .models import CategoriAlimento, Alimento, RegistoDiario, Refeicao, RefeicaoAlimento, Objetivo

admin.site.register(CategoriAlimento)
admin.site.register(Alimento)
admin.site.register(RegistoDiario)
admin.site.register(Refeicao)
admin.site.register(RefeicaoAlimento)
admin.site.register(Objetivo)