from django.shortcuts import render,redirect
from django.http import HttpResponse
from perfis.models import *
from posts.models import *

def add(request, perfil_id):
	if request.method=='POST':
		perfil = Perfil.objects.get(id=perfil_id)
		if len(perfil.postagens.all()) == 1 and perfil.postagens.all()[0].init == True:
			post = Post.objects.get(id=perfil.postagens.all()[0].id)
			post.init = False
			post.postagem = request.POST['postagem']
			post.save()
			return redirect('index')
		post = Post(user=perfil, postagem=request.POST['postagem'])
		post.save()
	return redirect('index')

