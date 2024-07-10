from django.contrib import admin
from .models import Produto,Fornecedor,Vendas,Pagamento

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    pass

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    pass

@admin.register(Vendas)
class VendasAdmin(admin.ModelAdmin):
    pass

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    pass