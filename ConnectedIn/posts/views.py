from django.core.files.storage import FileSystemStorage
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from rest_framework import generics
from django.utils import timezone
from datetime import datetime
from perfis.models import *
from posts.models import *
from posts.serializers import *


@transaction.atomic
def add(request, perfil_id):
    if request.method == 'POST':
        perfil = Perfil.objects.get(id=perfil_id)
        post = None
        message = 'Desculpe, houve um erro ao criar seu post!'
        with transaction.atomic():
            if len(perfil.postagens.all()) == 1 and perfil.postagens.all()[0].init == True:
                post = Post.objects.get(id=perfil.postagens.all()[0].id)
                post.init = False
                post.postagem = request.POST['postagem']
                post.created_at = timezone.make_aware(datetime.now(),timezone.get_current_timezone())
                post.save()
            else:
                post = Post(user=perfil, postagem=request.POST['postagem'])
                post.save()
            if request.FILES:
                for image in request.FILES.getlist('fotos_post'):
                    up_image = image
                    fs = FileSystemStorage()
                    name = fs.save(up_image.name, up_image)
                    url = fs.url(name)
                    foto = Image(post=post, foto=url)
                    foto.save()
            message = 'Post criado com sucesso!'
        message = Feedback(perfil=perfil,message=message)
        message.save()
        return redirect('index')

def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    if post in request.user.perfil.postagens.all() or request.user.is_superuser:
        post.delete()
    fed = Feedback(perfil=request.user.perfil,message='Postagem apagada!')
    fed.save()
    return redirect('index')


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name='post-list'
    '''permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )'''

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name='post-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

class PerfilList(generics.ListCreateAPIView):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    name='perfil-list'

class PerfilDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    name='perfil-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

class ImageList(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    name='image-list'
    '''permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )'''

class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    name='image-detail'
    '''permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )'''
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name='user-list'
    '''permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )'''

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name='user-detail'
    '''permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )'''