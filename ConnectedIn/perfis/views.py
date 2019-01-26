from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from django.shortcuts import render
from perfis.models import *
from posts.forms import PostModelForm
from django.core.paginator import Paginator, InvalidPage
from django.db import transaction

@login_required
def index(request):
    perfil_logado = get_perfil_logado(request)
    messages = Feedback.objects.filter(perfil=perfil_logado)
    feedbacks = []
    ITEMS_PER_PAGE = 10
    posts = getPosts(perfil_logado)
    paginator = Paginator(posts, ITEMS_PER_PAGE)
    page = request.GET.get('page',1)
    try:
        posts_page = paginator.get_page(page)
    except InvalidPage:
        posts_page = paginator.get_page(1)
    for msg in messages:
        feedbacks.append(msg.message)
        msg.delete()
    if perfil_logado.ativa == False or perfil_logado.bloqueado == True:
        return render(request,'perfis/transicao.html', {'perfil_logado': perfil_logado, 'messages':feedbacks})
    form = PostModelForm()
    if perfil_logado.usuario.is_superuser:
        return render(request, 'perfis/index.html', {'perfis': Perfil.objects.all(),
         'perfil_logado': perfil_logado, 'form':form, 'posts':posts_page, 'messages':feedbacks})
    return render(request, 'perfis/index.html', {'perfis': Perfil.objects.filter(ativa=True, bloqueado=False), 
        'perfil_logado': perfil_logado, 'form':form, 'posts':posts_page, 'messages':feedbacks})


def getPosts(perfil_logado):
    posts=[]
    for post in perfil_logado.postagens.all():
        posts.append(post)
    for perfil in perfil_logado.contatos.all():
        for post in perfil.postagens.all():
            posts.append(post)
    return boobleSort(posts)

def boobleSort(posts):
    for ind in range(len(posts)):
        for pos in range(len(posts)-1):
            if posts[ind].created_at > posts[pos].created_at:
                temp = posts[ind]
                posts[ind] = posts[pos]
                posts[pos] = temp
    return posts


@login_required
def exibir_perfil(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    messages = Feedback.objects.filter(perfil=get_perfil_logado(request))
    feedbacks = []
    for msg in messages:
        feedbacks.append(msg.message)
        msg.delete()
    posts = perfil.postagens.all()
    ITEMS_PER_PAGE = 5
    paginator = Paginator(posts, ITEMS_PER_PAGE)
    page = request.GET.get('page',1)
    try:
        posts_page = paginator.get_page(page)
    except InvalidPage:
        posts_page = paginator.get_page(1)
    form = PostModelForm()
    if perfil.bloqueado:
        perfil.error_mensage = 'Conta bloqueada pelos administradores!'
        return render(request, 'perfis/perfil.html',{'perfil_logado': get_perfil_logado(request), 'perfil':perfil})
    if perfil.ativa:
        perfil_logado = get_perfil_logado(request)
        perfil_logado.convidavel = perfil_logado.pode_convidar(perfil)
        if perfil_logado.usuario.is_superuser:
            return render(request, 'perfis/perfil.html',{'perfis': Perfil.objects.all(),
                'perfil': perfil,'perfil_logado': perfil_logado, 'form':form, 'posts':posts_page, 'messages':feedbacks})
        return render(request, 'perfis/perfil.html',{'perfil': perfil,
            'perfil_logado': perfil_logado, 'form':form, 'posts':posts_page, 'messages':feedbacks})
    else:
        perfil.error_mensage = 'Conta temporariamente desativada!'
        return render(request, 'perfis/perfil.html',{'perfil_logado': get_perfil_logado(request),'perfil':perfil})

@login_required
def convidar(request, perfil_id):
    perfil_a_convidar = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    if (perfil_logado.pode_convidar(perfil_a_convidar)):
        perfil_logado.convidar(perfil_a_convidar)
        fed = Feedback(perfil=perfil_logado,message='Convite enviado!')
        fed.save()
    return redirect('index')


def get_perfil_logado(request):
    return request.user.perfil


@login_required
def aceitar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.aceitar()
    fed = Feedback(perfil=get_perfil_logado(request),message='Você e '+convite.solicitante.nome+' agora são amigos!')
    fed.save()
    return redirect('index')


@login_required
def recusar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.recusar()
    fed = Feedback(perfil=get_perfil_logado(request),message='A solicitação foi cancelada!')
    fed.save()
    return redirect('index')


@login_required
def desfazer(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    perfil.desfazer(get_perfil_logado(request))
    fed = Feedback(perfil=get_perfil_logado(request),message='Você e '+perfil.nome+' não são mais amigos!')
    fed.save()
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
    return render(request, 'perfis/change_password.html', {'perfil_logado': get_perfil_logado(request),'form': form, })

def feed(request):
    userids = []
    for id in request.user.perfil.contatos.all():
        userids.append(id)
    userids.append(request.user.id)
    posts = Post.objects.filter(user_id_in=userids)[0:25]
    return render(request, 'feed.html', {'posts': posts})

def promover(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    if request.user.is_superuser:
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
        return render(request, 'perfis/desativar.html',{'perfil_logado':get_perfil_logado(request)})

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
        fed = Feedback(perfil=get_perfil_logado(request),message='Você bloqueou '+perfil.nome+'!')
        fed.save()
        return redirect('index')

def desbloquear(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    perfil.bloqueado = False
    perfil.save()
    fed = Feedback(perfil=get_perfil_logado(request),message='Você desbloqueou '+perfil.nome+'!')
    fed.save()
    return redirect('index')



def search(request):
    perfis = Perfil.objects.all();
    perfil_logado = get_perfil_logado(request)
    ITEMS_PER_PAGE = 5
    search = request.GET.get('word')
    if search:
        perfis = perfis.filter(nome__contains=search,bloqueado=False, ativa=True)
    paginator = Paginator(perfis, ITEMS_PER_PAGE)
    page = request.GET.get('page',1)
    try:
        perfis_search = paginator.get_page(page)
        for perfil in perfis_search:
            perfil.convidavel = perfil.pode_convidar(perfil_logado)
    except InvalidPage:
        perfis_search = paginator.get_page(1)
    if perfil_logado.usuario.is_superuser:
        return render(request, 'perfis/result_search.html', {'perfis_search':perfis_search, 
        'perfil_logado':perfil_logado, 'perfis':Perfil.objects.all()})
    return render(request, 'perfis/result_search.html', {
        'perfis_search':perfis_search, 'perfil_logado':perfil_logado
        })


def updatefoto(request):
    if request.method =='POST':
        up_image = request.FILES['foto']
        fs = FileSystemStorage()
        name = fs.save(up_image.name, up_image)
        url = fs.url(name)
        perfil = Perfil.objects.get(id=request.user.perfil.id) 
        perfil.foto = url
        perfil.save()
        fed = Feedback(perfil=get_perfil_logado(request),message='Sua foto do perfil foi atualizada!')
        fed.save()
        return redirect('exibir', perfil.id)