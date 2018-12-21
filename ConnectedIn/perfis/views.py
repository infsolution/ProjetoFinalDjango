from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from django.shortcuts import render

from perfis.models import Perfil, Convite


# Create your views here.

@login_required
def index(request):
    '''
    import random
    n = random.randint(0,100)
    return render(request, 'index.html', {'nome':'ely', 'n' : n})
    '''

    return render(request, 'index.html', {'perfis': Perfil.objects.all(),
                                          'perfil_logado': get_perfil_logado(request)})


@login_required
def exibir_perfil(request, perfil_id):
    # perfil = get(perfil_id)
    perfil = Perfil.objects.get(id=perfil_id)

    return render(request, 'perfil.html',
                  {'perfil': perfil,
                   'perfil_logado': get_perfil_logado(request)})


def get(perfil_id):
    if (perfil_id == 1):
        return Perfil('Firmo', 'azurefirmo@live.com',
                      'XXXXX-XXXX', 'AzureDOT')
    if (perfil_id == 2):
        return Perfil('Jamarola', 'jamarola@outlook.com',
                      'YYYYY-YYYY', 'Google')
    if (perfil_id == 3):
        return Perfil('Azure', 'azurefirmo@gmail.com',
                      'ZZZZZ-ZZZZ', 'Microsoft')


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
    for id in request.user.perfil.all():
        userids.append(id)

    userids.append(request.user.id)
    posts = Post.objects.filter(user_id_in=userids)[0:25]

    return render(request, 'feed.html', {'posts': posts})