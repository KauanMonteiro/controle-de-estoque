from django.db import models
from usuario.models import Usuario

RECEBIMENTO_STATUS = [
    ('pendente', 'Pendente'),
    ('pago', 'Pago'),
    ('cancelado', 'Cancelado'),
]

PAGAMENTO_STATUS = [
    ('pendente', 'Pendente'),
    ('pago', 'Pago'),
    ('cancelado', 'Cancelado'),
]
PARA_TODOS = 'todos'
PARA_DESTINATARIOS = 'destinatarios'
ESCOLHA_DESTINO = [
        (PARA_TODOS, 'Para todos os usuários'),
        (PARA_DESTINATARIOS, 'Para destinatários específicos'),
    ]

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
    preco = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome
        
class Vendas(models.Model):
    produto= models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_venda = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.produto.nome} - {self.data_venda}'   
    
class Pagamento(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_emissao = models.DateField(auto_now_add=True)
    data_vencimento = models.DateField()
    status = models.CharField(max_length=30, choices=PAGAMENTO_STATUS, default='pendente')

    def __str__(self) -> str:
        return f' Pagamento {self.fornecedor}-{self.data_vencimento}'
    
class Cliente(models.Model):
    nome = models.CharField(max_length=120)
    telefone = models.CharField(max_length=20)
    documento = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

class Mensagem(models.Model):
    titulo = models.CharField(max_length=100)
    aviso = models.TextField()
    data_de_criacao = models.DateTimeField(auto_now_add=True)
    destinatarios = models.ManyToManyField(Usuario, related_name='mensagens_enviadas', blank=True)
    remetente = models.ForeignKey(Usuario, related_name='mensagens_recebidas', on_delete=models.CASCADE)

    tipo_destino = models.CharField(max_length=20, choices=ESCOLHA_DESTINO, default=PARA_DESTINATARIOS)

    def __str__(self):
        return self.titulo