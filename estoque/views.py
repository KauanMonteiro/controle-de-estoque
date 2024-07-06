from django.shortcuts import get_object_or_404, render, redirect
from .models import Fornecedor, Produto

def home(request):
    return render(request, "pages/home.html")

def cadastrar_produto(request):
    fornecedor = Fornecedor.objects.all()

    if request.method == "POST":
        nome = request.POST.get('nome')
        quantidade = request.POST.get('quantidade')
        fornecedor_id = request.POST.get('fornecedor')  

        if len(nome.strip()) == 0:
            return redirect('cadastrar_produto')
        
        else:
            fornecedor = Fornecedor.objects.get(pk=fornecedor_id) 
            produto = Produto.objects.create(
                nome=nome,
                quantidade=quantidade,
                fornecedor=fornecedor  
            )
            return redirect('estoque')

    return render(request, "pages/cadastro_produto.html", {'fornecedor': fornecedor})


def cadastro_fornecedor(request):
    if request.method == 'POST':
        nome_fornecedor = request.POST.get('nome_fornecedor')
        contato = request.POST.get('contato')
        descricao = request.POST.get('descricao')

        fornecedor = Fornecedor.objects.create(
            nome_fornecedor=nome_fornecedor,
            contato=contato,
            descricao=descricao
        )
        return redirect('home') 

    return render(request, 'pages/cadastro_fornecedor.html')

def relatorio(request):
    ...

def estoque(request):
    fornecedor = Fornecedor.objects.all()
    produto = Produto.objects.all()

    return render(request, 'pages/estoque.html',{'produto':produto})

def editar_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    fornecedores = Fornecedor.objects.all()

    if request.method == 'POST':
        nome = request.POST.get('nome')
        quantidade = request.POST.get('quantidade')
        fornecedor_id = request.POST.get('fornecedor')

        if len(nome.strip()) == 0:
            return redirect('editar_produto', id=id)

        try:
            fornecedor = Fornecedor.objects.get(pk=fornecedor_id)
        except Fornecedor.DoesNotExist:
            return redirect('editar_produto', id=id)

        produto.nome = nome
        produto.quantidade = quantidade
        produto.fornecedor = fornecedor
        produto.save()

        return redirect('estoque')

    return render(request, 'pages/editar_produto.html', {'produto': produto, 'fornecedores': fornecedores})
