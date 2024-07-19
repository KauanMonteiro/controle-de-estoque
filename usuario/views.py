from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Usuario, CARGO_CHOICES, RegistroAcesso
from hashlib import sha256

def login(request):
    if request.session.get('usuario'):
        return redirect('/')
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

def cadastro(request):
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status, 'CARGO_CHOICES':CARGO_CHOICES})
    
def valida_cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        cargo = request.POST.get('cargo')  
        usuario = Usuario.objects.filter(email=email)

        if len(nome.strip()) == 0 or len(email.strip()) == 0:
            return redirect(reverse('cadastro') + '?status=1')

        if len(senha) < 8:
            return redirect(reverse('cadastro') + '?status=2')

        if usuario.exists():
            return redirect(reverse('cadastro') + '?status=3')

        try:
            senha = sha256(senha.encode()).hexdigest()
            usuario = Usuario(nome=nome, senha=senha, email=email, cargo=cargo) 
            usuario.save()

            return redirect(reverse('cadastro') + '?status=0')
        except Exception as e:
            print(e) 
            return redirect(reverse('cadastro') + '?status=4')

    return redirect(reverse('cadastro'))


def validar_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = Usuario.objects.filter(email=email).first()

        if usuario is not None and usuario.senha == sha256(senha.encode()).hexdigest():
            # Autenticando usuário
            request.session['usuario'] = usuario.id

            # Registrando entrada automática após login
            registro = RegistroAcesso(usuario=usuario, tipo_acesso='E')
            registro.save()

            return redirect('/')
        else:
            return redirect(reverse('login') + '?status=1')

    return redirect(reverse('login'))

def sair(request):
    if request.session.get('usuario'):
        # Registrando saída automática ao fazer logout
        usuario_id = request.session['usuario']
        usuario = Usuario.objects.get(id=usuario_id)
        registro = RegistroAcesso(usuario=usuario, tipo_acesso='S')
        registro.save()
        request.session.flush()
    
    return redirect(reverse('login'))