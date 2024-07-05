from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('relatorio/',views.relatorio, name='relatorio'),
    path('estoque/', views.estoque, name='estoque'),
    path('cadastrar_produto/',views.cadastrar_produto, name='cadastrar_produto')
]
