from django.contrib import admin
from .models import Produto,Fornecedor

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    pass

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    pass