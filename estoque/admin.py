from django.contrib import admin
from .models import Produto,Fornecedor,Vendas,Pagamento,Cliente,Mensagem

admin.site.register(Fornecedor)
admin.site.register(Produto)
admin.site.register(Vendas)
admin.site.register(Pagamento)
admin.site.register(Cliente)
admin.site.register(Mensagem)