# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.views.generic.base import View
from usuarios.forms import RegistrarUsuarioForm
from django.contrib.auth.models import User
from perfis.models import *
from posts.models import Post
from usuarios.models import *
from django.core.mail import send_mail
from django.conf import settings
from random import randint
from datetime import datetime, timedelta, date
from django.utils import timezone
class RegistrarUsuarioView(View):

	def get(self, request):
		return render(request, 'usuarios/registrar.html')

	def post(self, request):
		form = RegistrarUsuarioForm(request.POST)

		if (form.is_valid()) :
			dados = form.cleaned_data

			usuario = User.objects.create_user(dados['nome'],
						   dados['email'],
						   dados['senha'])

			perfil = Perfil(nome = usuario.username, 
							nome_empresa = dados['nome_empresa'],
							telefone = dados['telefone'],
							usuario = usuario)
			perfil.save()
			post = Post(user=perfil, postagem='Opa, nenhuma postagem!', init=True)
			post.save()
			message = Feedback(perfil=perfil,message='Perfil criado com sucesso.')
			message.save()
			return redirect('login')
		
		return render(request, 'usuarios/registrar.html', {'form': form})



def reset(request):
	if request.method == 'POST':
		email = request.POST['email']
		try:
			user = User.objects.get(email=email)
			subject = 'Reset password'	
			message = 'Clique neste link http://localhost:8000/usuarios/redefinir/%(codigo)s ou copie e cole no seu navegador para criar uma nova senha para sua conta no SosiAll'
			codigo = get_token()
			cod = Codigo(user=user,code=codigo)
			cod.save()
			context = {
				'email':user.email,
				'codigo':codigo,
			}
			message = message % context
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, 
             [settings.CONTACT_EMAIL])	
			return redirect('login')
		except Exception as e:
			return render(request, 'usuarios/resetar_senha.html',
				{'msg_error':'O email "'+email+'" não existe!'})	
	return render(request, 'usuarios/resetar_senha.html')


def redefinir(request, codigo):
	try:
		cod = Codigo.objects.get(code=codigo)
		now = datetime.now()
		if dif_date(now,cod.date_send) <= 1440:
			return render(request,'usuarios/resetar_senha_confirmacao.html',{'usuario':cod.user})
	except Exception as e:
		print(e)
		return redirect('login')


def get_token():
	token = ''
	for num in range(0,32):
		char = randint(1,4)
		if char == 1:
			token += str(chr(randint(48,57)))
		elif char == 2:
			token += str(chr(randint(65,90)))
		else:
			token += str(chr(randint(97,122)))
	return token

def dif_date(date1, date2):
	date1 = str(date1)
	date2= str(date2)
	now = datetime.strptime(date1[0:19], "%Y-%m-%d %H:%M:%S")
	send = datetime.strptime(date2[0:19], "%Y-%m-%d %H:%M:%S")
	return ((now - send).total_seconds()/60)

def confirmar_reset(request):
	if request.method == 'POST':
		user = User.objects.get(id=request.POST['user_id'])
		if request.POST['password'] == request.POST['password_1']:
			user.set_password(request.POST['password'])
			user.save()
			return redirect('login')
		return render(request,'usuarios/resetar_senha_confirmacao.html',
			{'usuario':user, 'msg_error':'As senhas não são iguais!'})
	return redirect('login')