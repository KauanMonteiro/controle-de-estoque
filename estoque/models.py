from django.db import models

class Fornecedor(models.Model):
    nome_fornecedor = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20,default='')
    documento = models.CharField(max_length=20,default='')
    rua = models.CharField(max_length=250,default='')
    numero = models.CharField(max_length=10,default='')
    bairro = models.CharField(max_length=100, default='')
    cidade = models.CharField(max_length=100,default='')
    estado = models.CharField(max_length=2,default='')
    
    def __str__(self):
        return self.nome_fornecedor
    

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField(default=0)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome
        

class Vendas(models.Model):
    produto= models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_venda = models.DateField(auto_now_add=True)

def __str__(self) -> str:
        return f'{self.produto.nome} - {self.data_venda}'