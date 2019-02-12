from django.core.files.storage import FileSystemStorage
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, exceptions
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import datetime
from perfis.models import *
from posts.models import *
from posts.serializers import *
from . import permissions as per


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
        fed.type_message='danger'
        fed.save()
        return redirect('index')
    else:
        fed = Feedback(perfil=request.user.perfil,message='Você só pode apagar suas postagens!')
        fed.type_message='danger'
        fed.save()
        return redirect('index')

def to_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    comment = Comments(post=post, user=request.user.perfil, content=request.POST.get('comment'))
    comment.save()
    #return redirect('index')
    return redirect('http://localhost:8000#'+post.postagem)

def to_react(request, post_id):
    post = Post.objects.get(id=post_id)
    reaction = Reaction(post=post, user=request.user.perfil, reaction=request.POST.get('reaction'))
    reaction.save()
    return redirect('http://localhost:8000#'+post.postagem)
def to_share(request, post_id):
    post = Post.objects.get(id=post_id)
    myShare = Post(user=request.user.perfil, postagem=post.postagem, compartilhado=post.user)
    myShare.save()
    if post.imagens.all():
        for image in post.imagens.all():
            foto = Image(post=myShare, foto=image.foto)
            foto.save()
    fed = Feedback(perfil=request.user.perfil,message='Postagem compartilhada na sua linha do tempo!')
    fed.type_message='success'
    fed.save()
    return redirect('http://localhost:8000#'+post.postagem)




#API METODOS
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_class = (TokenAuthentication,)
    #permission_class = (IsOwnerUpdate)    
    name='post-list'
    

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_class = (TokenAuthentication,)
    permission_classes =(IsOwnerUpdate,)
    name='post-detail'

class PerfilList(generics.ListCreateAPIView):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    name='perfil-list'

class PerfilDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    permission_class = (IsOwnerUpdate, IsOwnerOrReadOnly)
    name='perfil-detail'
    

class ImageList(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    name='image-list'

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

class PostImageList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostImageSerializers
    authentication_class = (TokenAuthentication,)
    permission_class = (IsAuthenticated,IsOwnerUpdate)
    name='postimage-list'

class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializers
    authentication_class = (TokenAuthentication)
    name='post-create'
    def perform_create(self, serializer):
        if self.request.method == 'POST':
            post = Post(user=self.request.user.perfil, postagem=self.request.POST['postagem'])
            post.save()
        if self.request.FILES:
            for image in self.request.FILES.getlist('fotos'):
                up_image = image
                fs = FileSystemStorage()
                name = fs.save(up_image.name, up_image)
                url = fs.url(name)
                foto = Image(post=post, foto=url)
                foto.save()
        return Response(serializer.data)

class CommentsList(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class=CommentSerializers
    authentication_class = (TokenAuthentication)
    name='comments-list'

class CommentsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class=CommentSerializers
    authentication_class = (TokenAuthentication)
    name='comments-detail'