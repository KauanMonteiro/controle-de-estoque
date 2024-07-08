from django.shortcuts import get_object_or_404, render, redirect
from .models import Fornecedor, Produto,Vendas

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
        telefone = request.POST.get('telefone')
        documento = request.POST.get('documento')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')

        fornecedor = Fornecedor.objects.create(
            nome_fornecedor=nome_fornecedor,
            telefone=telefone,
            documento=documento,
            rua=rua,
            numero=numero,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
        )
        return redirect('home') 

    return render(request, 'pages/cadastro_fornecedor.html')

def relatorio(request):
    ...

def estoque(request):
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

def lista_fornecedores(request):
    fornecedor = Fornecedor.objects.all()

    return render(request, 'pages/lista_fornecedores.html',{'fornecedor':fornecedor})


def editar_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, pk=id)

    if request.method == 'POST':
        nome_fornecedor = request.POST.get('nome_fornecedor')
        telefone = request.POST.get('telefone')
        documento = request.POST.get('documento')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')

        fornecedor.nome_fornecedor = nome_fornecedor
        fornecedor.telefone = telefone
        fornecedor.documento = documento
        fornecedor.rua = rua
        fornecedor.numero = numero
        fornecedor.bairro = bairro
        fornecedor.cidade = cidade
        fornecedor.estado = estado

        fornecedor.save()

        return redirect('lista_fornecedores')

    return render(request, 'pages/editar_fornecedor.html', {'fornecedor': fornecedor})

def vendas(request):
    if request.method == 'POST':
        produto_vendido_id = request.POST.get('produto')
        quantidade = int(request.POST.get('quantidade'))  

        produto = Produto.objects.get(pk=produto_vendido_id)

        if produto.quantidade >= quantidade:
            produto.quantidade -= quantidade
            produto.save()

            venda = Vendas.objects.create(
                produto=produto,
                quantidade=quantidade
            )
                
            return redirect('estoque')  
        else:
            return redirect('home')  
    
    produtos = Produto.objects.all()
    return render(request, 'pages/registrar_venda.html', {'produtos': produtos})

def excluir_produto(request, id):
    produto = Produto.objects.get(pk=id)

    if request.method == "POST":
        produto.delete()
        return redirect('home')
    
def excluir_fornecedor(request, id):
    fornecedor = Fornecedor.objects.get(pk=id)
    
    if request.method == "POST":
        fornecedor.delete()
        return redirect('home')
    
    