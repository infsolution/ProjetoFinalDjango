from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from perfis.models import *
from posts.models import *


def add(request, perfil_id):
    if request.method == 'POST':
        perfil = Perfil.objects.get(id=perfil_id)
        post = None
        if len(perfil.postagens.all()) == 1 and perfil.postagens.all()[0].init == True:
            post = Post.objects.get(id=perfil.postagens.all()[0].id)
            post.init = False
            post.postagem = request.POST['postagem']
            post.save()
        else:
            post = Post(user=perfil, postagem=request.POST['postagem'])
            post.save()
        if request.FILES:
            for image in request.FILES.getlist('fotos_post'):
                print(image)
                up_image = image
                fs = FileSystemStorage()
                name = fs.save(up_image.name, up_image)
                url = fs.url(name)
                foto = Image(post=post, foto=url)
                foto.save()
        return redirect('index')


def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    if post in request.user.perfil.postagens.all() or request.user.is_superuser:
        post.delete()
    return redirect('index')


'''class DialogsView(View):
    def get(self, request):
        chats = Chat.objects.filter(members__in=[request.user.id])
        return render(request, 'posts/templates/posts/dialogs.html', {'user_profile': request.user, 'chats': chats})


class MessagesView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(
            request,
            'users/messages.html',
            {
                'user_profile': request.user,
                'chat': chat,
                'form': MessageForm()
            }
        )

    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('users:messages', kwargs={'chat_id': chat_id}))


class CreateDialogView(View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(
            c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('users:messages', kwargs={'chat_id': chat.id}))'''
