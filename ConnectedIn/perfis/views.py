from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from django.shortcuts import render
from perfis.models import *

@login_required
def index(request):
    perfil_logado = get_perfil_logado(request)
    if perfil_logado.ativa == False or perfil_logado.bloqueado == True:
        return render(request,'perfis/transicao.html', {'perfil_logado': perfil_logado})
    return render(request, 'perfis/index.html', {'perfis': Perfil.objects.filter(ativa=True), 'perfil_logado': perfil_logado})


@login_required
def exibir_perfil(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    if perfil.ativa:
        perfil_logado = get_perfil_logado(request)
        perfil_logado.convidavel = perfil_logado.pode_convidar(perfil)
        return render(request, 'perfis/perfil.html',{'perfil': perfil,'perfil_logado': perfil_logado})
    else:
        return render(request, 'perfis/perfil.html',{'deactivated':'Conta temporariamente desativada!',
            'perfil_logado': get_perfil_logado(request)})
@login_required
def convidar(request, perfil_id):
    perfil_a_convidar = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    if (perfil_logado.pode_convidar(perfil_a_convidar)):
        perfil_logado.convidar(perfil_a_convidar)

    return redirect('index')


def get_perfil_logado(request):
    return request.user.perfil


@login_required
def aceitar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.aceitar()
    return redirect('index')


@login_required
def recusar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.recusar()
    return redirect('index')


@login_required
def desfazer(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    perfil.desfazer(get_perfil_logado(request))
    return redirect('index')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'perfis/change_password.html', {
        'form': form
    })

def feed(request):
    userids = []
    for id in request.user.perfil.contatos.all():
        userids.append(id)
    userids.append(request.user.id)
    posts = Post.objects.filter(user_id_in=userids)[0:25]
    return render(request, 'feed.html', {'posts': posts})

def promover(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    if request.user.is_superuser == True:
        usuario = perfil.usuario
        usuario.is_superuser = 1
        usuario.save()
    else:
        return render(request, 'perfis/perfil.html',{'perfil': perfil,
            'perfil_logado': get_perfil_logado(request), 'error':'Você não é admin'}) 
    return render(request, 'perfis/perfil.html',{'perfil': perfil,
        'perfil_logado': get_perfil_logado(request)})

def desativar(request):
    if request.method == 'POST':
        perfil = Perfil.objects.get(usuario=request.user)
        perfil.ativa = False
        perfil.justificativa = request.POST['justificativa']
        perfil.save()
        return redirect('login')

    else:
        return render(request, 'perfis/desativar.html')

def reativar(request):
    if request.method == 'POST':
        perfil = Perfil.objects.get(usuario=request.user)
        perfil.ativa = True
        perfil.save()
    return redirect('index')

def bloquear(request, perfil_id):
    if request.user.is_superuser:
        perfil = Perfil.objects.get(id=perfil_id)
        perfil.bloqueado = True
        perfil.save()
        return redirect('index')
