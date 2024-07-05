from django.db import models

class Fornecedor(models.Model):
    nome_fornecedor = models.CharField(max_length=150)
    contato =  models.CharField(max_length=150, default='')
    descricao = models.CharField(max_length=190,default='', null=True, blank=True)
    
    def __str__(self):
        return self.nome_fornecedor
    

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField(default=0)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome