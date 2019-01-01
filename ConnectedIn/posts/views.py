from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect
from django.http import HttpResponse
from perfis.models import *
from posts.models import *

def add(request, perfil_id):
	if request.method=='POST':
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
