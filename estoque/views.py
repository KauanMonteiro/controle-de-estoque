from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html")

def cadastrar_produto(request):
    ...

def relatorio(request):
    ...

def estoque(request):
    ...