from django.db import models

ADMINISTRADOR = 'Admin'
GERENTE_ESTOQUE = 'GestorEstoque'
GERENTE_COMPRAS = 'GestorCompras'
GERENTE_CLIENTES = 'GestorClientes'
ANALISTA_FINANCEIRO = 'AnalistaFinanceiro'

CARGO_CHOICES = [
    (ADMINISTRADOR, 'Administrador'),
    (GERENTE_ESTOQUE, 'Gerente de Estoque'),
    (GERENTE_COMPRAS, 'Gerente de Compras'),
    (GERENTE_CLIENTES, 'Gerente de Clientes'),
    (ANALISTA_FINANCEIRO, 'Analista Financeiro'),
]

class Usuario(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField()
    senha = models.CharField(max_length=64)
    ativo = models.BooleanField(default=False)
    cargo = models.CharField(max_length=18, choices=CARGO_CHOICES)

    def __str__(self):
        return self.nome
