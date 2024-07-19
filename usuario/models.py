from datetime import timezone
from django.db import models

ADMINISTRADOR = 'Admin'
GERENTE_ESTOQUE = 'GestorEstoque'
ANALISTA_FINANCEIRO = 'AnalistaFinanceiro'

CARGO_CHOICES = [
    (ADMINISTRADOR, 'Administrador'),
    (GERENTE_ESTOQUE, 'Gerente de Estoque'),
    (ANALISTA_FINANCEIRO, 'Analista Financeiro'),
]

class Usuario(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=64)
    ativo = models.BooleanField(default=False)
    cargo = models.CharField(max_length=18, choices=CARGO_CHOICES)

    def __str__(self):
        return self.nome
    
class RegistroAcesso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_acesso = models.CharField(max_length=1, choices=(('E', 'Entrada'), ('S', 'Saída')))
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_acesso_display()} em {self.data_hora}"