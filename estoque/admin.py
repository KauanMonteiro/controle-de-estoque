from django.contrib import admin
from .models import Produto,Fornecedor,Vendas

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    pass

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    pass

@admin.register(Vendas)
class VendasAdmin(admin.ModelAdmin):
    pass