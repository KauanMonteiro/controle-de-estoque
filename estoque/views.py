from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from .models import Fornecedor, Produto,Vendas,Pagamento, PAGAMENTO_STATUS,Cliente, Mensagem
from django.db.models import Sum,F
from django.utils.timezone import now  
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.db.models.functions import TruncMonth
from usuario.models import Usuario,RegistroAcesso


def home(request):
    if 'usuario' not in request.session:
        return redirect('login')

    usuario_id = request.session['usuario']
    usuario = Usuario.objects.get(pk=usuario_id)

    return render(request, "pages/home.html", {'usuario': usuario})

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
        produto_id = request.POST.get('produto')
        quantidade = request.POST.get('quantidade')
        cliente_id = request.POST.get('cliente')
        
        # Convertendo o ID e a quantidade para inteiros
        try:
            produto_id = int(produto_id)
            quantidade = int(quantidade)
            cliente_id = int(cliente_id)
        except ValueError:
            return HttpResponseBadRequest('IDs e quantidade devem ser números inteiros.')

        # Obtendo as instâncias necessárias
        try:
            produto = Produto.objects.get(id=produto_id)
            cliente = Cliente.objects.get(id=cliente_id)
        except Produto.DoesNotExist:
            return HttpResponseBadRequest('Produto não encontrado.')
        except Cliente.DoesNotExist:
            return HttpResponseBadRequest('Cliente não encontrado.')

        # Verificando a quantidade disponível
        if produto.quantidade < quantidade:
            return HttpResponseBadRequest('Quantidade solicitada excede a disponibilidade do produto.')

        # Atualizando a quantidade do produto
        produto.quantidade -= quantidade
        produto.save()

        # Criando a venda
        venda = Vendas.objects.create(
            produto=produto,
            quantidade=quantidade,
            cliente=cliente
        )
        
        # Resposta de sucesso
        return HttpResponse('Venda registrada com sucesso!')
    
    # Lógica para métodos GET ou outras ações
    clientes = Cliente.objects.all()
    produtos = Produto.objects.all()
    return render(request, 'pages/registrar_venda.html', {'clientes': clientes, 'produtos': produtos})

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
    pagamento = Pagamento.objects.all().order_by('-data_vencimento') 
    registros = RegistroAcesso.objects.all().order_by('-data_hora')
    mes_atual = now().month
    ano_atual = now().year

    # Calcula o mês e o ano do mês anterior
    mes_anterior = mes_atual - 1 if mes_atual > 1 else 12
    ano_anterior = ano_atual if mes_atual > 1 else ano_atual - 1

    # Faturamento por Mês
    vendas_por_mes = Vendas.objects.filter(
        data_venda__month__in=[mes_atual, mes_anterior],
        data_venda__year__in=[ano_atual, ano_anterior]
    ).annotate(
        mes_venda=TruncMonth('data_venda')
    ).values('mes_venda').annotate(
        total_faturamento=Sum(F('produto__preco') * F('quantidade'))
    ).order_by('mes_venda')  

    meses = [venda['mes_venda'].strftime('%b %Y') for venda in vendas_por_mes]
    faturamento = [venda['total_faturamento'] or 0 for venda in vendas_por_mes]

    # Gráfico de Faturamento
    plt.figure(figsize=(10, 6))
    plt.plot(meses, faturamento, marker='o', linestyle='-')
    plt.title('Faturamento por Mês')
    plt.xlabel('Mês')
    plt.ylabel('Faturamento')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_faturamento_png = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    # Vendas mensais
    vendas_por_mes_quantidade = Vendas.objects.filter(
        data_venda__month__in=[mes_atual, mes_anterior],
        data_venda__year__in=[ano_atual, ano_anterior]
    ).annotate(
        mes_venda=TruncMonth('data_venda')
    ).values('mes_venda').annotate(
        total=Sum('quantidade')
    ).order_by('mes_venda')

    meses_quantidade = [venda['mes_venda'].strftime('%b %Y') for venda in vendas_por_mes_quantidade]
    quantidades_mes = [venda['total'] or 0 for venda in vendas_por_mes_quantidade]

    # Gráfico de Vendas Mensais
    plt.figure(figsize=(10, 6))
    plt.plot(meses_quantidade, quantidades_mes, marker='o', linestyle='-')
    plt.xlabel('Meses')
    plt.ylabel('Vendas')
    plt.title('Vendas Mensais')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png2 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    # Produtos mais vendidos
    vendas_por_produto = Vendas.objects.values('produto__nome').annotate(total=Sum('quantidade')).order_by('-total')[:10]

    produtos = [venda['produto__nome'] for venda in vendas_por_produto]
    quantidades = [venda['total'] or 0 for venda in vendas_por_produto]

    # Gráfico de Produtos Mais Vendidos
    plt.figure(figsize=(10, 6))
    plt.bar(produtos, quantidades)
    plt.ylabel('Quantidade Vendida')
    plt.title('Produtos Mais Vendidos')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    # Despesas por fornecedor no mês atual
    despesas_por_fornecedor_mes = Pagamento.objects.filter(
        data_vencimento__month=mes_atual, 
        data_vencimento__year=ano_atual
    ).values('fornecedor__nome_fornecedor').annotate(
        total=Sum('valor')
    ).order_by('-total')[:10]

    fornecedor = [despesa['fornecedor__nome_fornecedor'] for despesa in despesas_por_fornecedor_mes]
    valor = [despesa['total'] or 0 for despesa in despesas_por_fornecedor_mes]

    # Gráfico de Despesas por Fornecedor
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

    # Vendas por Cliente no mês atual
    vendas_mes = Vendas.objects.filter(
        data_venda__month=mes_atual,
        data_venda__year=ano_atual
    ).annotate(
        total=F('quantidade') * F('produto__preco')  # Adiciona o valor total da venda
    )
    vendas_por_cliente = vendas_mes.values('cliente__nome').annotate(total=Sum('quantidade')).order_by('-total')[:10]

    clientes = [venda['cliente__nome'] for venda in vendas_por_cliente]
    quantidades_clientes = [venda['total'] or 0 for venda in vendas_por_cliente]

    # Gráfico de Participação dos Clientes
    vendas = vendas_mes.values('cliente').annotate(total_vendas=Sum('quantidade'))
    
    cliente_nomes = [Cliente.objects.get(id=v['cliente']).nome for v in vendas]
    quantidades_vendas = [v['total_vendas'] for v in vendas]

    plt.figure(figsize=(8, 8))
    plt.pie(quantidades_vendas, labels=cliente_nomes, autopct='%1.1f%%', colors=plt.cm.Paired(range(len(cliente_nomes))))
    plt.title('Participação dos Clientes nas Vendas')
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_clientes_png = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return render(request, 'pages/dashboard.html', {
        'cliente': clientes,
        'grafico_mais_vendidos': image_png,
        'grafico_vendas_mes': image_png2,
        'pagamento': pagamento,
        'image_despesas_png': image_despesas_png,
        'despesas_por_fornecedor_mes': despesas_por_fornecedor_mes,
        'image_faturamento_png': image_faturamento_png,
        'vendas_mes': vendas_mes,
        'registros': registros,
        'grafico_clientes': image_clientes_png,
    })
def area_despesas(request): 
    pagamento = Pagamento.objects.exclude(status='pago').exclude(status='cancelado').order_by('-data_vencimento')
    pagamento_pagos_cancelados = Pagamento.objects.exclude(status='pendente').order_by('-data_vencimento')

    return render(request, 'pages/area_despesas.html', {
        'pagamento': pagamento,
        'pagamento_pagos_cancelados': pagamento_pagos_cancelados
    })

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
    
def cadastro_cliente(request):
    cliente = Cliente.objects.all()

    if request.method == "POST":
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        documento = request.POST.get('documento')

        cliente = Cliente.objects.create (
            nome = nome,
            telefone = telefone,
            documento = documento
        )
        return redirect('lista_clientes')
    return render(request,'pages/cadastro_cliente.html')

def lista_clientes(request):
    clientes = Cliente.objects.all()

    return render(request,'pages/lista_cliente.html',{'clientes':clientes})

def excluir_cliente(request,id):
    cliente = get_object_or_404(Cliente, pk=id)

    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')

def editar_cliente(request,id):
    cliente = get_object_or_404(Cliente, pk=id)
    
    if request.method =='POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        documento = request.POST.get('documento')

        cliente.nome = nome
        cliente.telefone = telefone
        cliente.documento = documento

        cliente.save()
        return redirect('lista_clientes')
    
    return render(request,'pages/editar_cliente.html',{'cliente':cliente})

def recebimentos(request):
    vendas = Vendas.objects.all().order_by('-data_venda')

    for venda in vendas:
        venda.total = venda.produto.preco * venda.quantidade

    hoje = datetime.now()
    mes_atual = hoje.month
    ano_atual = hoje.year

    vendas_mes = Vendas.objects.filter(data_venda__month=mes_atual, data_venda__year=ano_atual)

    for venda_mes in vendas_mes:
        venda_mes.total = venda_mes.produto.preco * venda_mes.quantidade

    return render(request, 'pages/recebimentos.html', {'vendas': vendas, 'vendas_mes': vendas_mes})

def avisos(request):
    if 'usuario' not in request.session:
        return redirect('login')

    usuario_id = request.session['usuario']
    usuario = Usuario.objects.get(pk=usuario_id)
    mensagem = Mensagem.objects.filter(destinatarios=usuario).order_by('-id')

    return render(request,'pages/avisos.html',{'mensagem':mensagem,'usuario':usuario})

def enviar_mensagem(request):
    if 'usuario' not in request.session:
        return redirect('login')

    usuario_id = request.session['usuario']
    remetente = get_object_or_404(Usuario, pk=usuario_id)
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        aviso = request.POST.get('aviso')
        tipo_destino = request.POST.get('tipo_destino')

        if tipo_destino == 'todos':
            destinatarios = Usuario.objects.all() 
        elif tipo_destino == 'destinatarios':
            destinatario_id = request.POST.get('destinatario')  
            destinatario = get_object_or_404(Usuario, pk=destinatario_id)
            destinatarios = [destinatario]

        mensagem = Mensagem.objects.create(
            titulo=titulo,
            aviso=aviso,
            remetente=remetente,
            tipo_destino=tipo_destino  
        )
        mensagem.destinatarios.set(destinatarios)
        mensagem.save()

        return redirect('home') 
    
    usuarios = Usuario.objects.exclude(pk=usuario_id) 

    return render(request, 'pages/enviar_aviso.html', {'usuarios': usuarios, 'remetente': remetente})