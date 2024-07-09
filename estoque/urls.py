from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('estoque/', views.estoque, name='estoque'),
    path('cadastrar_produto/',views.cadastrar_produto, name='cadastrar_produto'),
    path('cadastro_fornecedor/',views.cadastro_fornecedor, name='cadastro_fornecedor'),
    path('editar_produto/<int:id>/', views.editar_produto, name='editar_produto'),
    path('lista_fornecedores/', views.lista_fornecedores, name='lista_fornecedores'),
    path('editar_fornecedor/<int:id>/', views.editar_fornecedor, name='editar_fornecedor'),
    path('registrar_vendas/',views.vendas, name='vendas'),
    path('estoque/delete/<int:id>/',views.excluir_produto, name='excluir_produto'),
    path('fornecedor/delete/<int:id>/',views.excluir_fornecedor, name='excluir_fornecedor')
]

