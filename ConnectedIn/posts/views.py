from django.shortcuts import render,redirect
from django.http import HttpResponse
from perfis.models import *
from posts.models import *

def add(request, perfil_id):
	if request.method=='POST':
		perfil = Perfil.objects.get(id=perfil_id)
		post = Post(user=perfil, postagem=request.POST['postagem'])
		post.save()
	return redirect('index')

