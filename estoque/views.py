from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from .models import Fornecedor, Produto,Vendas,Pagamento, PAGAMENTO_STATUS
from django.db.models import Sum
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.db.models.functions import TruncMonth


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

def dashboard(request):
    pagamento = Pagamento.objects.all()
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    vendas_por_mes = Vendas.objects.annotate(
        mes_venda=TruncMonth('data_venda')
    ).values('mes_venda').annotate(
        total=Sum('quantidade')
    ).order_by('mes_venda')

    meses = [venda['mes_venda'].strftime('%b %Y') for venda in vendas_por_mes]
    quantidades_mes = [venda['total'] for venda in vendas_por_mes]

    plt.figure(figsize=(10, 6))
    plt.plot(meses, quantidades_mes, marker='o', linestyle='-')
    plt.xlabel('Meses')
    plt.ylabel('Vendas')
    plt.title('Vendas Mensais')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png2 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    vendas_por_produto = Vendas.objects.values('produto__nome').annotate(total=Sum('quantidade')).order_by('-total')[:10]

    produtos = [venda['produto__nome'] for venda in vendas_por_produto]
    quantidades = [venda['total'] for venda in vendas_por_produto]

    plt.figure(figsize=(10, 6))
    plt.bar(produtos, quantidades)
    plt.ylabel('Quantidade Vendida')
    plt.title('Produtos mais vendidos')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    despesas_por_fornecedor_mes = Pagamento.objects.filter(data_vencimento__month=mes_atual, data_vencimento__year=ano_atual)\
        .values('fornecedor__nome_fornecedor')\
        .annotate(total=Sum('valor'))\
        .order_by('-total')[:10]

    fornecedor = [despesa['fornecedor__nome_fornecedor'] for despesa in despesas_por_fornecedor_mes]
    valor = [despesa['total'] for despesa in despesas_por_fornecedor_mes]

    plt.figure(figsize=(10, 6))
    plt.bar(fornecedor, valor, color='salmon')
    plt.xlabel('Fornecedor')
    plt.ylabel('Valor da Despesa')
    plt.title('Despesas por Fornecedor no Mês Atual')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_despesas_png = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return render(request, 'pages/dashboard.html', {
        'grafico_mais_vendidos': image_png,
        'grafico_vendas_mes': image_png2,
        'pagamento': pagamento,
        'image_despesas_png': image_despesas_png,
        'despesas_por_fornecedor_mes': despesas_por_fornecedor_mes,
    })

def area_despesas(request): 
    pagamento = Pagamento.objects.exclude(status='pago').exclude(status='cancelado')
    pagamento_pagos_cancelados = Pagamento.objects.exclude(status='pendente')

    return render(request, 'pages/area_despesas.html', {'pagamento': pagamento, 'pagamento_pagos_cancelados':pagamento_pagos_cancelados})

def cadastro_pagamento(request):
    fornecedores = Fornecedor.objects.all()

    if request.method == 'POST':
        fornecedor_id = request.POST.get('fornecedor')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data_vencimento = request.POST.get('data_vencimento')
        status = request.POST.get('status')

        pagamento = Pagamento.objects.create(
            fornecedor_id=fornecedor_id,
            descricao=descricao,
            valor=valor,
            data_vencimento=data_vencimento,
            status=status
        )

        return redirect('area_despesas')

    return render(request, 'pages/cadastro_pagamento.html', {'fornecedores': fornecedores, 'PAGAMENTO_STATUS': PAGAMENTO_STATUS})

def editar_pagamento(request, id):
    pagamento = get_object_or_404(Pagamento, pk=id)
    fornecedores = Fornecedor.objects.all()
    
    if request.method == 'POST':
        fornecedor_id = request.POST.get('fornecedor')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data_vencimento = request.POST.get('data_vencimento')
        status = request.POST.get('status')

        fornecedor = get_object_or_404(Fornecedor, pk=fornecedor_id)

        pagamento.fornecedor = fornecedor
        pagamento.descricao = descricao
        pagamento.valor = valor
        pagamento.data_vencimento = data_vencimento
        pagamento.status = status

        pagamento.save()
        return redirect('area_despesas')
    
    return render(request, 'pages/editar_pagamento.html', {
        'pagamento': pagamento,
        'fornecedores': fornecedores,
        'PAGAMENTO_STATUS': PAGAMENTO_STATUS
    })

def excluir_despesas(request, id):
    pagamento = get_object_or_404(Pagamento, pk=id)

    if request.method == "POST":
        pagamento.delete()
        return redirect('home')